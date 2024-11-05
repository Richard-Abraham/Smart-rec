import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// Export the middleware function as default
export default function middleware(request: NextRequest) {
  // Get the token from localStorage instead of cookies for client-side storage
  const isAuthPage = request.nextUrl.pathname.startsWith('/login') || 
                     request.nextUrl.pathname.startsWith('/signup');

  // Check if we're on the client side
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('token');

    if (!token && !isAuthPage) {
      return NextResponse.redirect(new URL('/login', request.url));
    }

    if (token && isAuthPage) {
      return NextResponse.redirect(new URL('/dashboard', request.url));
    }
  }

  return NextResponse.next();
}

// Configure which routes to run middleware on
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
}; 