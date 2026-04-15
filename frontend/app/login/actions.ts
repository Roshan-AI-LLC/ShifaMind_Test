"use server"

export async function requestAccess(formData: FormData) {
  const name = formData.get("name") as string
  const email = formData.get("email") as string
  const organization = formData.get("organization") as string

  // We need an email provider to send an email securely from the server.
  // Resend is used here via its REST API (no dependencies required).
  const RESEND_API_KEY = process.env.RESEND_API_KEY

  if (!RESEND_API_KEY) {
    console.error("RESEND_API_KEY is not set in environment variables.")
    return { 
      success: false, 
      error: "Server configuration error: Email provider API key is missing. Please contact setup." 
    }
  }

  try {
    const res = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${RESEND_API_KEY}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        // 'onboarding@resend.dev' is available automatically for testing domains
        from: "ShifaMind Platform <onboarding@resend.dev>",
        to: "mohammedsameersyed1@gmail.com",
        subject: `Platform Access Request: ${name} (${organization})`,
        html: `
          <div style="font-family: sans-serif; max-width: 500px; padding: 20px;">
            <h2>New Access Request</h2>
            <p>A new user has requested access to the ShifaMind platform.</p>
            <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
              <tr>
                <td style="padding: 8px; border-bottom: 1px solid #eee; width: 120px;"><strong>Name</strong></td>
                <td style="padding: 8px; border-bottom: 1px solid #eee;">${name}</td>
              </tr>
              <tr>
                <td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>Email</strong></td>
                <td style="padding: 8px; border-bottom: 1px solid #eee;"><a href="mailto:${email}">${email}</a></td>
              </tr>
              <tr>
                <td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>Organization</strong></td>
                <td style="padding: 8px; border-bottom: 1px solid #eee;">${organization}</td>
              </tr>
            </table>
          </div>
        `
      })
    })

    if (!res.ok) {
      const data = await res.json()
      console.error("Resend API error:", data)
      return { success: false, error: "Email service rejected the request. Please try again later." }
    }

    return { success: true }
  } catch (err: any) {
    console.error("Request access action error:", err)
    return { success: false, error: err?.message || "An internal error occurred." }
  }
}
