export const metadata = {
  title: 'OpenTelemetry Demo',
  description: 'Next.js + Django + MySQL with OpenTelemetry',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
