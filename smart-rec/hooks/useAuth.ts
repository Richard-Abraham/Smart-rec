import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export function useAuth(requireAuth: boolean = true) {
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('token');
    const isAuthPage = window.location.pathname.includes('/login') || 
                      window.location.pathname.includes('/signup');

    if (!token && requireAuth && !isAuthPage) {
      router.push('/login');
    }

    if (token && isAuthPage) {
      router.push('/dashboard');
    }
  }, [router, requireAuth]);
} 