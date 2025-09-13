-- Create profiles table
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID REFERENCES auth.users ON DELETE CASCADE PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Enable RLS on profiles
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Create policy for profiles
CREATE POLICY "Users can view own profile" ON public.profiles
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can insert own profile" ON public.profiles
    FOR INSERT WITH CHECK (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON public.profiles
    FOR UPDATE USING (auth.uid() = id);

-- Create clothes table
CREATE TABLE IF NOT EXISTS public.clothes (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    profile_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    color TEXT,
    size TEXT,
    image_url TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Enable RLS on clothes
ALTER TABLE public.clothes ENABLE ROW LEVEL SECURITY;

-- Create policies for clothes
CREATE POLICY "Users can view own clothes" ON public.clothes
    FOR SELECT USING (auth.uid() = profile_id);

CREATE POLICY "Users can insert own clothes" ON public.clothes
    FOR INSERT WITH CHECK (auth.uid() = profile_id);

CREATE POLICY "Users can update own clothes" ON public.clothes
    FOR UPDATE USING (auth.uid() = profile_id);

CREATE POLICY "Users can delete own clothes" ON public.clothes
    FOR DELETE USING (auth.uid() = profile_id);

-- Create function to handle new user signup
CREATE OR REPLACE FUNCTION public.handle_new_user() 
RETURNS trigger AS $$
BEGIN
  INSERT INTO public.profiles (id, email)
  VALUES (NEW.id, NEW.email);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create trigger for new user signup
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE PROCEDURE public.handle_new_user();

-- Create storage bucket policy for clothing images
INSERT INTO storage.buckets (id, name, public) VALUES ('clothing-items', 'clothing-items', true);

-- Create policy for clothing images bucket
CREATE POLICY "Anyone can view clothing images" ON storage.objects FOR SELECT USING (bucket_id = 'clothing-items');
CREATE POLICY "Users can upload clothing images" ON storage.objects FOR INSERT WITH CHECK (bucket_id = 'clothing-items' AND auth.role() = 'authenticated');
CREATE POLICY "Users can update own clothing images" ON storage.objects FOR UPDATE USING (bucket_id = 'clothing-items' AND auth.uid()::text = (storage.foldername(name))[1]);
CREATE POLICY "Users can delete own clothing images" ON storage.objects FOR DELETE USING (bucket_id = 'clothing-items' AND auth.uid()::text = (storage.foldername(name))[1]);