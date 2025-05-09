
/**
 * Utility for managing SEO metadata and Open Graph tags
 */

// Set page title and meta description
export const setPageMeta = (title: string, description?: string) => {
  document.title = title ? `${title} | Portal Licitações` : 'Portal Licitações';
  
  // Update meta description
  if (description) {
    let metaDescription = document.querySelector('meta[name="description"]');
    if (!metaDescription) {
      metaDescription = document.createElement('meta');
      metaDescription.setAttribute('name', 'description');
      document.head.appendChild(metaDescription);
    }
    metaDescription.setAttribute('content', description);
  }
};

// Set Open Graph tags
export const setOpenGraph = (data: {
  title?: string;
  description?: string;
  image?: string;
  url?: string;
  type?: 'website' | 'article' | 'profile';
}) => {
  const { title, description, image, url, type = 'website' } = data;
  
  // Helper to set or create meta tag
  const setMetaTag = (property: string, content?: string) => {
    if (!content) return;
    
    let tag = document.querySelector(`meta[property="${property}"]`);
    if (!tag) {
      tag = document.createElement('meta');
      tag.setAttribute('property', property);
      document.head.appendChild(tag);
    }
    tag.setAttribute('content', content);
  };
  
  // Set Open Graph tags
  setMetaTag('og:title', title);
  setMetaTag('og:description', description);
  setMetaTag('og:image', image);
  setMetaTag('og:url', url || window.location.href);
  setMetaTag('og:type', type);
  
  // Set Twitter card tags
  setMetaTag('twitter:card', 'summary_large_image');
  setMetaTag('twitter:title', title);
  setMetaTag('twitter:description', description);
  setMetaTag('twitter:image', image);
};

// Hook to easily use SEO utilities in components
export const useSeo = () => {
  return {
    setPageMeta,
    setOpenGraph
  };
};
