import Link from "next/link";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-b from-blue-50 to-white px-4">
      <main className="flex w-full max-w-4xl flex-col items-center text-center">
        <h1 className="text-5xl font-bold tracking-tight text-gray-900 sm:text-6xl">
          Telugu AI Tutor
        </h1>
        <p className="mt-6 text-lg leading-8 text-gray-600 max-w-2xl">
          Master Telugu with personalized AI-powered lessons, adaptive practice, and intelligent feedback.
          Your journey to fluency starts here.
        </p>

        <div className="mt-10 flex items-center gap-4">
          <Link
            href="/register"
            className="rounded-md bg-blue-600 px-6 py-3 text-base font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
          >
            Get Started
          </Link>
          <Link
            href="/login"
            className="rounded-md bg-white px-6 py-3 text-base font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
          >
            Sign In
          </Link>
        </div>

        <div className="mt-16 grid grid-cols-1 gap-8 sm:grid-cols-3 max-w-3xl">
          <div className="flex flex-col items-center">
            <div className="text-4xl mb-3">🎯</div>
            <h3 className="text-lg font-semibold text-gray-900">Personalized Learning</h3>
            <p className="mt-2 text-sm text-gray-600">
              Adaptive lessons tailored to your goals and learning style
            </p>
          </div>

          <div className="flex flex-col items-center">
            <div className="text-4xl mb-3">💬</div>
            <h3 className="text-lg font-semibold text-gray-900">AI Chat Practice</h3>
            <p className="mt-2 text-sm text-gray-600">
              Practice conversations with intelligent feedback on grammar and vocabulary
            </p>
          </div>

          <div className="flex flex-col items-center">
            <div className="text-4xl mb-3">📈</div>
            <h3 className="text-lg font-semibold text-gray-900">Track Progress</h3>
            <p className="mt-2 text-sm text-gray-600">
              Monitor your improvement with detailed analytics and skill graphs
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}
