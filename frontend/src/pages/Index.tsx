
import React from "react";
import { ThemeToggle } from "@/components/theme/ThemeToggle";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";

// Import the new section components
import HeroSection from "@/components/landing/HeroSection";
import FeaturesSection from "@/components/landing/FeaturesSection";
import TestimonialsSection from "@/components/landing/TestimonialsSection";
import AboutSection from "@/components/landing/AboutSection";
import ContactSection from "@/components/landing/ContactSection";
import FooterSection from "@/components/landing/FooterSection";

const Index = () => {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Header/NavBar */}
      <header className="bg-background py-4 px-6 border-b border-border shadow-sm">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <h1 className="text-2xl font-bold text-foreground">CotAi Licitação Hub</h1>
          <div className="flex items-center gap-4">
            <ThemeToggle />
            <Button variant="ghost" asChild>
              <Link to="/demo/dashboard">Demonstração</Link>
            </Button>
            <Button asChild>
              <Link to="/login">Login</Link>
            </Button>
          </div>
        </div>
      </header>

      {/* Page Sections */}
      <HeroSection />
      <FeaturesSection />
      <TestimonialsSection />
      <AboutSection />
      <ContactSection />
      <FooterSection />
    </div>
  );
};

export default Index;
