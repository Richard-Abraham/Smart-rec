import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || "https://qrhyssmvqxjkpblncpqw.supabase.co"
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFyaHlzc212cXhqa3BibG5jcHF3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzAzNzMzNjMsImV4cCI6MjA0NTk0OTM2M30.a_P15cO60iJO4XVYbitCnWubE6cy3bV8wB8MEDw5X00"

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error('Missing Supabase environment variables')
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey) 