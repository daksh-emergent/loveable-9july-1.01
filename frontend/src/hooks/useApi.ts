// Custom hooks for API data fetching using React Query
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useCallback } from 'react';

import {
  heroApi,
  featuresApi,
  testimonialsApi,
  processStepsApi,
  specificationsApi,
  navigationApi,
  footerApi,
  siteSettingsApi,
  newsletterApi,
  contactApi,
  searchApi,
  analyticsApi,
  handleApiError,
  HeroContent,
  Feature,
  Testimonial,
  ProcessStep,
  Specification,
  NavigationItem,
  FooterSection,
  SiteSettings,
  NewsletterSignup,
  ContactFormData,
  PageView,
} from '@/services/api';

// Query keys
export const QUERY_KEYS = {
  HERO: 'hero',
  FEATURES: 'features',
  TESTIMONIALS: 'testimonials',
  PROCESS_STEPS: 'process-steps',
  SPECIFICATIONS: 'specifications',
  NAVIGATION: 'navigation',
  FOOTER: 'footer',
  SITE_SETTINGS: 'site-settings',
  SEARCH: 'search',
} as const;

// Hero Content Hooks
export const useHeroContent = () => {
  return useQuery({
    queryKey: [QUERY_KEYS.HERO],
    queryFn: async () => {
      const response = await heroApi.get();
      return response.data;
    },
    staleTime: 60 * 60 * 1000, // 1 hour
  });
};

export const useCreateHeroContent = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: heroApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.HERO] });
    },
    onError: (error) => {
      console.error('Failed to create hero content:', handleApiError(error));
    },
  });
};

// Features Hooks
export const useFeatures = (category?: string) => {
  return useQuery({
    queryKey: [QUERY_KEYS.FEATURES, category],
    queryFn: async () => {
      const response = await featuresApi.getAll(category);
      return response.data;
    },
    staleTime: 30 * 60 * 1000, // 30 minutes
  });
};

export const useCreateFeature = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: featuresApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.FEATURES] });
    },
    onError: (error) => {
      console.error('Failed to create feature:', handleApiError(error));
    },
  });
};

export const useUpdateFeature = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<Feature> }) =>
      featuresApi.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.FEATURES] });
    },
    onError: (error) => {
      console.error('Failed to update feature:', handleApiError(error));
    },
  });
};

// Testimonials Hooks
export const useTestimonials = (limit: number = 10) => {
  return useQuery({
    queryKey: [QUERY_KEYS.TESTIMONIALS, limit],
    queryFn: async () => {
      const response = await testimonialsApi.getAll(limit);
      return response.data;
    },
    staleTime: 30 * 60 * 1000, // 30 minutes
  });
};

export const useCreateTestimonial = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: testimonialsApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.TESTIMONIALS] });
    },
    onError: (error) => {
      console.error('Failed to create testimonial:', handleApiError(error));
    },
  });
};

// Process Steps Hooks
export const useProcessSteps = (stepType: string = 'process') => {
  return useQuery({
    queryKey: [QUERY_KEYS.PROCESS_STEPS, stepType],
    queryFn: async () => {
      const response = await processStepsApi.getAll(stepType);
      return response.data;
    },
    staleTime: 30 * 60 * 1000, // 30 minutes
  });
};

export const useCreateProcessStep = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: processStepsApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.PROCESS_STEPS] });
    },
    onError: (error) => {
      console.error('Failed to create process step:', handleApiError(error));
    },
  });
};

// Specifications Hooks
export const useSpecifications = () => {
  return useQuery({
    queryKey: [QUERY_KEYS.SPECIFICATIONS],
    queryFn: async () => {
      const response = await specificationsApi.getAll();
      return response.data;
    },
    staleTime: 30 * 60 * 1000, // 30 minutes
  });
};

export const useCreateSpecification = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: specificationsApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.SPECIFICATIONS] });
    },
    onError: (error) => {
      console.error('Failed to create specification:', handleApiError(error));
    },
  });
};

// Navigation Hooks
export const useNavigation = (navType: string = 'main') => {
  return useQuery({
    queryKey: [QUERY_KEYS.NAVIGATION, navType],
    queryFn: async () => {
      const response = await navigationApi.getAll(navType);
      return response.data;
    },
    staleTime: 2 * 60 * 60 * 1000, // 2 hours
  });
};

export const useCreateNavigationItem = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: navigationApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.NAVIGATION] });
    },
    onError: (error) => {
      console.error('Failed to create navigation item:', handleApiError(error));
    },
  });
};

// Footer Hooks
export const useFooter = () => {
  return useQuery({
    queryKey: [QUERY_KEYS.FOOTER],
    queryFn: async () => {
      const response = await footerApi.getAll();
      return response.data;
    },
    staleTime: 2 * 60 * 60 * 1000, // 2 hours
  });
};

export const useCreateFooterSection = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: footerApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.FOOTER] });
    },
    onError: (error) => {
      console.error('Failed to create footer section:', handleApiError(error));
    },
  });
};

// Site Settings Hooks
export const useSiteSettings = () => {
  return useQuery({
    queryKey: [QUERY_KEYS.SITE_SETTINGS],
    queryFn: async () => {
      const response = await siteSettingsApi.get();
      return response.data;
    },
    staleTime: 2 * 60 * 60 * 1000, // 2 hours
  });
};

export const useCreateSiteSettings = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: siteSettingsApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.SITE_SETTINGS] });
    },
    onError: (error) => {
      console.error('Failed to create site settings:', handleApiError(error));
    },
  });
};

// Newsletter Hooks
export const useNewsletterSignup = () => {
  return useMutation({
    mutationFn: newsletterApi.signup,
    onError: (error) => {
      console.error('Failed to signup for newsletter:', handleApiError(error));
    },
  });
};

// Contact Form Hooks
export const useContactForm = () => {
  return useMutation({
    mutationFn: contactApi.submit,
    onError: (error) => {
      console.error('Failed to submit contact form:', handleApiError(error));
    },
  });
};

// Search Hooks
export const useSearch = (query: string, contentType?: string, enabled: boolean = true) => {
  return useQuery({
    queryKey: [QUERY_KEYS.SEARCH, query, contentType],
    queryFn: async () => {
      const response = await searchApi.search(query, contentType);
      return response.data;
    },
    enabled: enabled && query.length > 0,
    staleTime: 10 * 60 * 1000, // 10 minutes
  });
};

// Analytics Hooks
export const useTrackPageView = () => {
  return useMutation({
    mutationFn: analyticsApi.trackPageView,
    onError: (error) => {
      console.error('Failed to track page view:', handleApiError(error));
    },
  });
};

// Custom hook for page view tracking
export const usePageViewTracking = () => {
  const trackPageView = useTrackPageView();
  
  const trackPage = useCallback((path: string) => {
    trackPageView.mutate({
      page_path: path,
      referrer: document.referrer,
      user_agent: navigator.userAgent,
      session_id: sessionStorage.getItem('session_id') || undefined,
    });
  }, [trackPageView]);
  
  return { trackPage };
};

// Loading state helper
export const useLoadingStates = () => {
  const heroQuery = useHeroContent();
  const featuresQuery = useFeatures();
  const testimonialsQuery = useTestimonials();
  const processStepsQuery = useProcessSteps();
  const specificationsQuery = useSpecifications();
  const navigationQuery = useNavigation();
  const footerQuery = useFooter();
  const siteSettingsQuery = useSiteSettings();
  
  return {
    isLoading: 
      heroQuery.isLoading ||
      featuresQuery.isLoading ||
      testimonialsQuery.isLoading ||
      processStepsQuery.isLoading ||
      specificationsQuery.isLoading ||
      navigationQuery.isLoading ||
      footerQuery.isLoading ||
      siteSettingsQuery.isLoading,
    
    isError: 
      heroQuery.isError ||
      featuresQuery.isError ||
      testimonialsQuery.isError ||
      processStepsQuery.isError ||
      specificationsQuery.isError ||
      navigationQuery.isError ||
      footerQuery.isError ||
      siteSettingsQuery.isError,
    
    errors: {
      hero: heroQuery.error,
      features: featuresQuery.error,
      testimonials: testimonialsQuery.error,
      processSteps: processStepsQuery.error,
      specifications: specificationsQuery.error,
      navigation: navigationQuery.error,
      footer: footerQuery.error,
      siteSettings: siteSettingsQuery.error,
    }
  };
};