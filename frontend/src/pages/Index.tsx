
import React, { useEffect } from "react";
import { usePageViewTracking } from "@/hooks/useApi";
import Navbar from "@/components/Navbar";
import Hero from "@/components/Hero";
import HumanoidSection from "@/components/HumanoidSection";
import SpecsSection from "@/components/SpecsSection";
import DetailsSection from "@/components/DetailsSection";
import ImageShowcaseSection from "@/components/ImageShowcaseSection";
import Features from "@/components/Features";
import Testimonials from "@/components/Testimonials";
import Newsletter from "@/components/Newsletter";
import MadeByHumans from "@/components/MadeByHumans";
import Footer from "@/components/Footer";

const Index = () => {
  const { trackPage } = usePageViewTracking();

  // OPTIMIZED: Single IntersectionObserver for all animations
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("animate-fade-in");
            observer.unobserve(entry.target); // Stop observing once animated
          }
        });
      },
      { 
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px' // Trigger animation earlier for better UX
      }
    );
    
    // Observe all animation elements at once
    const elements = document.querySelectorAll(".animate-on-scroll");
    elements.forEach((el) => observer.observe(el));
    
    return () => {
      // Cleanup all observers
      elements.forEach((el) => observer.unobserve(el));
    };
  }, []);

  // OPTIMIZED: Debounced smooth scrolling for anchor links
  useEffect(() => {
    const handleAnchorClick = (e: Event) => {
      const target = e.target as HTMLAnchorElement;
      const href = target.getAttribute('href');
      
      if (!href?.startsWith('#')) return;
      
      e.preventDefault();
      
      const targetId = href.substring(1);
      if (!targetId) {
        // Scroll to top
        window.scrollTo({
          top: 0,
          behavior: 'smooth'
        });
        return;
      }
      
      const targetElement = document.getElementById(targetId);
      if (!targetElement) return;
      
      // Calculate offset for mobile/desktop
      const offset = window.innerWidth < 768 ? 100 : 80;
      
      window.scrollTo({
        top: targetElement.offsetTop - offset,
        behavior: 'smooth'
      });
    };

    // Use event delegation for better performance
    document.addEventListener('click', (e) => {
      const target = e.target as HTMLElement;
      const anchor = target.closest('a[href^="#"]');
      if (anchor) {
        handleAnchorClick(e);
      }
    });

    return () => {
      document.removeEventListener('click', handleAnchorClick);
    };
  }, []);

  // Track page view for analytics
  useEffect(() => {
    trackPage('/');
  }, [trackPage]);

  return (
    <div className="min-h-screen">
      <Navbar />
      <main className="space-y-4 sm:space-y-8"> {/* Reduced space on mobile */}
        <Hero />
        <HumanoidSection />
        <SpecsSection />
        <DetailsSection />
        <ImageShowcaseSection />
        <Features />
        <Testimonials />
        <Newsletter />
        <MadeByHumans />
      </main>
      <Footer />
    </div>
  );
};

export default Index;
