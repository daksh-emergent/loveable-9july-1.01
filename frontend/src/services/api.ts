// API service layer for backend communication
import { QueryClient } from '@tanstack/react-query';

const API_BASE_URL = import.meta.env.VITE_REACT_APP_BACKEND_URL || process.env.REACT_APP_BACKEND_URL;

export interface ApiResponse<T> {
  success: boolean;
  message: string;
  data: T;
}

export interface PaginatedResponse<T> {
  success: boolean;
  message: string;
  data: T[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

// Generic API request function
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> {
  const url = `${API_BASE_URL}/api/content${endpoint}`;
  
  const defaultOptions: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(url, defaultOptions);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
}

// Hero Content API
export interface HeroContent {
  id: string;
  title: string;
  subtitle: string;
  description: string;
  cta_text: string;
  cta_link: string;
  background_image: string;
  lottie_animation_url?: string;
  hero_image?: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
  order: number;
}

export const heroApi = {
  get: (): Promise<ApiResponse<HeroContent>> => 
    apiRequest<HeroContent>('/hero'),
  
  create: (data: Partial<HeroContent>): Promise<ApiResponse<HeroContent>> =>
    apiRequest<HeroContent>('/hero', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
};

// Features API
export interface Feature {
  id: string;
  title: string;
  description: string;
  icon_svg: string;
  category: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
  order: number;
}

export const featuresApi = {
  getAll: (category?: string): Promise<ApiResponse<Feature[]>> => {
    const params = category ? `?category=${encodeURIComponent(category)}` : '';
    return apiRequest<Feature[]>(`/features${params}`);
  },
  
  create: (data: Partial<Feature>): Promise<ApiResponse<Feature>> =>
    apiRequest<Feature>('/features', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  
  update: (id: string, data: Partial<Feature>): Promise<ApiResponse<Feature>> =>
    apiRequest<Feature>(`/features/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),
};

// Testimonials API
export interface Testimonial {
  id: string;
  content: string;
  author: string;
  role: string;
  company: string;
  gradient: string;
  background_image: string;
  rating: number;
  created_at: string;
  updated_at: string;
  is_active: boolean;
  order: number;
}

export const testimonialsApi = {
  getAll: (limit: number = 10): Promise<ApiResponse<Testimonial[]>> => 
    apiRequest<Testimonial[]>(`/testimonials?limit=${limit}`),
  
  create: (data: Partial<Testimonial>): Promise<ApiResponse<Testimonial>> =>
    apiRequest<Testimonial>('/testimonials', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
};

// Process Steps API
export interface ProcessStep {
  id: string;
  number: string;
  title: string;
  description: string;
  image_url: string;
  step_type: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
  order: number;
}

export const processStepsApi = {
  getAll: (stepType: string = 'process'): Promise<ApiResponse<ProcessStep[]>> => 
    apiRequest<ProcessStep[]>(`/process-steps?step_type=${stepType}`),
  
  create: (data: Partial<ProcessStep>): Promise<ApiResponse<ProcessStep>> =>
    apiRequest<ProcessStep>('/process-steps', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
};

// Specifications API
export interface Specification {
  id: string;
  section_title: string;
  section_subtitle: string;
  content: string;
  section_number: string;
  background_image?: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
  order: number;
}

export const specificationsApi = {
  getAll: (): Promise<ApiResponse<Specification[]>> => 
    apiRequest<Specification[]>('/specifications'),
  
  create: (data: Partial<Specification>): Promise<ApiResponse<Specification>> =>
    apiRequest<Specification>('/specifications', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
};

// Navigation API
export interface NavigationItem {
  id: string;
  label: string;
  href: string;
  target: string;
  nav_type: string;
  parent_id?: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
  order: number;
}

export const navigationApi = {
  getAll: (navType: string = 'main'): Promise<ApiResponse<NavigationItem[]>> => 
    apiRequest<NavigationItem[]>(`/navigation?nav_type=${navType}`),
  
  create: (data: Partial<NavigationItem>): Promise<ApiResponse<NavigationItem>> =>
    apiRequest<NavigationItem>('/navigation', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
};

// Footer API
export interface FooterSection {
  id: string;
  title: string;
  content: string;
  section_type: string;
  links: Array<{ text: string; url: string }>;
  created_at: string;
  updated_at: string;
  is_active: boolean;
  order: number;
}

export const footerApi = {
  getAll: (): Promise<ApiResponse<FooterSection[]>> => 
    apiRequest<FooterSection[]>('/footer'),
  
  create: (data: Partial<FooterSection>): Promise<ApiResponse<FooterSection>> =>
    apiRequest<FooterSection>('/footer', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
};

// Site Settings API
export interface SiteSettings {
  id: string;
  site_title: string;
  site_description: string;
  logo_url: string;
  favicon_url: string;
  primary_color: string;
  secondary_color: string;
  contact_email: string;
  contact_phone?: string;
  social_links: Record<string, string>;
  analytics_code?: string;
  seo_keywords: string[];
  created_at: string;
  updated_at: string;
  is_active: boolean;
  order: number;
}

export const siteSettingsApi = {
  get: (): Promise<ApiResponse<SiteSettings>> => 
    apiRequest<SiteSettings>('/site-settings'),
  
  create: (data: Partial<SiteSettings>): Promise<ApiResponse<SiteSettings>> =>
    apiRequest<SiteSettings>('/site-settings', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
};

// Newsletter API
export interface NewsletterSignup {
  email: string;
  name?: string;
  interests?: string[];
  source?: string;
}

export const newsletterApi = {
  signup: (data: NewsletterSignup): Promise<ApiResponse<any>> =>
    apiRequest<any>('/newsletter/signup', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
};

// Contact Form API
export interface ContactFormData {
  name: string;
  email: string;
  subject: string;
  message: string;
  phone?: string;
  company?: string;
}

export const contactApi = {
  submit: (data: ContactFormData): Promise<ApiResponse<any>> =>
    apiRequest<any>('/contact', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
};

// Search API
export interface SearchResult {
  id: string;
  content_type: string;
  title?: string;
  description?: string;
  content?: string;
  author?: string;
  role?: string;
  order: number;
}

export const searchApi = {
  search: (query: string, contentType?: string): Promise<ApiResponse<SearchResult[]>> => {
    const params = new URLSearchParams({ query });
    if (contentType) params.append('content_type', contentType);
    return apiRequest<SearchResult[]>(`/search?${params.toString()}`);
  },
};

// Analytics API
export interface PageView {
  page_path: string;
  referrer?: string;
  user_agent?: string;
  session_id?: string;
  country?: string;
  device_type?: string;
}

export const analyticsApi = {
  trackPageView: (data: PageView): Promise<ApiResponse<any>> =>
    apiRequest<any>('/analytics/pageview', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
};

// Create a configured QueryClient
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 3,
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
      refetchOnWindowFocus: false,
      refetchOnReconnect: true,
    },
    mutations: {
      retry: 1,
    },
  },
});

// Error handling utility
export const handleApiError = (error: any) => {
  if (error.response?.data?.message) {
    return error.response.data.message;
  }
  if (error.message) {
    return error.message;
  }
  return 'An unexpected error occurred';
};