#!/usr/bin/env python3
"""
Database operations script for Drip Drop
Run this script to initialize the database tables and policies
"""

import os
import sys
from supabase import create_client, Client
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()
    
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
    
    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        print("Error: SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in .env file")
        sys.exit(1)
    
    # Create Supabase client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    
    try:
        # Create profiles table
        print("Creating profiles table...")
        profiles_sql = """
        CREATE TABLE IF NOT EXISTS public.profiles (
            id UUID REFERENCES auth.users ON DELETE CASCADE PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
        );
        """
        supabase.rpc('exec_sql', {'sql': profiles_sql}).execute()
        
        # Create clothes table
        print("Creating clothes table...")
        clothes_sql = """
        CREATE TABLE IF NOT EXISTS public.clothes (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            profile_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            primary_color TEXT,
            secondary_color TEXT,
            size TEXT,
            image_url TEXT NOT NULL,
            is_owned BOOLEAN DEFAULT true NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
        );
        """
        supabase.rpc('exec_sql', {'sql': clothes_sql}).execute()

        # Add is_owned column to existing clothes table (for migration)
        print("Adding is_owned column to existing clothes table...")
        migration_sql = """
        ALTER TABLE public.clothes
        ADD COLUMN IF NOT EXISTS is_owned BOOLEAN DEFAULT true NOT NULL;
        """
        supabase.rpc('exec_sql', {'sql': migration_sql}).execute()

        # Create accessories table
        print("Creating accessories table...")
        accessories_sql = """
        CREATE TABLE IF NOT EXISTS public.accessories (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            profile_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            primary_color TEXT,
            secondary_color TEXT,
            size TEXT,
            image_url TEXT NOT NULL,
            is_owned BOOLEAN DEFAULT true NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
        );
        """
        supabase.rpc('exec_sql', {'sql': accessories_sql}).execute()

        # Create outfits table
        print("Creating outfits table...")
        outfits_sql = """
        CREATE TABLE IF NOT EXISTS public.outfits (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            profile_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
            name TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
        );
        """
        supabase.rpc('exec_sql', {'sql': outfits_sql}).execute()

        # Create outfit_items junction table
        print("Creating outfit_items junction table...")
        outfit_items_sql = """
        CREATE TABLE IF NOT EXISTS public.outfit_items (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            outfit_id UUID NOT NULL REFERENCES public.outfits(id) ON DELETE CASCADE,
            item_type TEXT NOT NULL CHECK (item_type IN ('clothing', 'accessory')),
            item_id UUID NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
        );
        """
        supabase.rpc('exec_sql', {'sql': outfit_items_sql}).execute()

        print("Database tables created successfully!")

        # Enable RLS
        print("Enabling Row Level Security...")
        rls_sql = """
        ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
        ALTER TABLE public.clothes ENABLE ROW LEVEL SECURITY;
        ALTER TABLE public.accessories ENABLE ROW LEVEL SECURITY;
        ALTER TABLE public.outfits ENABLE ROW LEVEL SECURITY;
        ALTER TABLE public.outfit_items ENABLE ROW LEVEL SECURITY;
        """
        supabase.rpc('exec_sql', {'sql': rls_sql}).execute()
        
        print("Row Level Security enabled!")
        print("Database initialization completed successfully!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()