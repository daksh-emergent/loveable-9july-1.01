
import React, { useRef } from "react";
import { useTestimonials } from "@/hooks/useApi";

interface TestimonialProps {
  content: string;
  author: string;
  role: string;
  company: string;
  gradient: string;
  backgroundImage?: string;
}

const TestimonialCard = ({
  content,
  author,
  role,
  company,
  backgroundImage = "/background-section1.png"
}: TestimonialProps) => {
  return <div className="bg-cover bg-center rounded-lg p-8 h-full flex flex-col justify-between text-white transform transition-transform duration-300 hover:-translate-y-2 relative overflow-hidden" style={{
    backgroundImage: `url('${backgroundImage}')`
  }}>
      <div className="absolute top-0 right-0 w-24 h-24 bg-white z-10"></div>
      
      <div className="relative z-0">
        <p className="text-xl mb-8 font-medium leading-relaxed pr-20">{`"${content}"`}</p>
        <div>
          <h4 className="font-semibold text-xl">{author}</h4>
          <p className="text-white/80">{role}, {company}</p>
        </div>
      </div>
    </div>;
};

const Testimonials = () => {
  const sectionRef = useRef<HTMLDivElement>(null);
  
  // Fetch testimonials from API
  const { data: testimonials, isLoading, error } = useTestimonials(10);

  // Loading state
  if (isLoading) {
    return (
      <section className="py-12 bg-white relative" id="testimonials" ref={sectionRef}>
        <div className="section-container">
          <div className="flex items-center gap-4 mb-6">
            <div className="animate-pulse">
              <div className="h-8 bg-gray-300 rounded w-32"></div>
            </div>
          </div>
          
          <div className="animate-pulse mb-12">
            <div className="h-12 bg-gray-300 rounded w-64 mb-4"></div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {[...Array(4)].map((_, index) => (
              <div key={index} className="animate-pulse bg-gray-300 rounded-lg h-64"></div>
            ))}
          </div>
        </div>
      </section>
    );
  }

  // Error state
  if (error) {
    return (
      <section className="py-12 bg-white relative" id="testimonials" ref={sectionRef}>
        <div className="section-container">
          <div className="text-center">
            <div className="text-red-600 mb-4">Failed to load testimonials</div>
            <button 
              onClick={() => window.location.reload()} 
              className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
            >
              Retry
            </button>
          </div>
        </div>
      </section>
    );
  }

  return <section className="py-12 bg-white relative" id="testimonials" ref={sectionRef}> {/* Reduced from py-20 */}
      <div className="section-container opacity-0 animate-on-scroll">
        <div className="flex items-center gap-4 mb-6">
          <div className="pulse-chip">
            <span className="inline-flex items-center justify-center w-5 h-5 rounded-full bg-pulse-500 text-white mr-2">04</span>
            <span>Testimonials</span>
          </div>
        </div>
        
        <h2 className="text-5xl font-display font-bold mb-12 text-left">What others say</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {testimonials?.map((testimonial, index) => (
            <TestimonialCard 
              key={testimonial.id} 
              content={testimonial.content} 
              author={testimonial.author} 
              role={testimonial.role} 
              company={testimonial.company}
              gradient={testimonial.gradient} 
              backgroundImage={testimonial.background_image} 
            />
          ))}
        </div>
      </div>
    </section>;
};

export default Testimonials;
