/* HTTP Basic Auth gate for the Rise knowledge base.
 *
 * Runs at the edge on every request, so the content is never sent to an
 * unauthenticated client. This matters here: the dossier is a single page with
 * all of its content inline, so a client-side password prompt would be theatre:
 * the whole model would sit in view-source behind it.
 *
 * The password is read from the DOSSIER_PASSWORD environment variable, set in
 * the Netlify UI (Site configuration → Environment variables). It is never
 * committed: these repos run gitleaks on commit and a hardcoded secret is a
 * blocking finding.
 */

const REALM = "Rise knowledge base";
const USER = "rise";

/* Length-independent comparison, so response time does not leak the password. */
function safeEqual(a, b) {
  const enc = new TextEncoder();
  const x = enc.encode(a);
  const y = enc.encode(b);
  let diff = x.length ^ y.length;
  const n = Math.max(x.length, y.length);
  for (let i = 0; i < n; i++) diff |= (x[i] ?? 0) ^ (y[i] ?? 0);
  return diff === 0;
}

function challenge() {
  return new Response("Authentication required.", {
    status: 401,
    headers: {
      "WWW-Authenticate": `Basic realm="${REALM}", charset="UTF-8"`,
      "Cache-Control": "no-store",
      "Content-Type": "text/plain; charset=utf-8",
    },
  });
}

export default async (request, context) => {
  const expected = Netlify.env.get("DOSSIER_PASSWORD");

  /* Fail closed. An unset variable must never mean "let everyone in". */
  if (!expected) {
    return new Response("Gate not configured.", {
      status: 503,
      headers: { "Cache-Control": "no-store" },
    });
  }

  const header = request.headers.get("authorization") ?? "";
  if (!header.startsWith("Basic ")) return challenge();

  let user, pass;
  try {
    const decoded = atob(header.slice(6));
    const split = decoded.indexOf(":");
    if (split < 0) return challenge();
    user = decoded.slice(0, split);
    pass = decoded.slice(split + 1);
  } catch {
    return challenge();
  }

  if (!safeEqual(user, USER) || !safeEqual(pass, expected)) return challenge();

  /* Authenticated: hand off to the static site, and make sure no shared cache
   * ever holds a gated page. */
  const response = await context.next();
  response.headers.set("Cache-Control", "private, no-store");
  response.headers.set("X-Robots-Tag", "noindex, nofollow");
  return response;
};

export const config = { path: "/*" };
