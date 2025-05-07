
import React from "react";
import { Link } from "react-router-dom";

const FooterSection: React.FC = () => {
  return (
    <footer className="bg-muted px-6 py-8 border-t border-border">
      <div className="max-w-7xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-lg font-semibold mb-4">CotAi Licitação Hub</h3>
            <p className="text-muted-foreground text-sm">
              Soluções inovadoras com inteligência artificial para gerenciamento de licitações
            </p>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold mb-4">Links Rápidos</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/" className="text-muted-foreground hover:text-primary transition-colors">
                  Início
                </Link>
              </li>
              <li>
                <Link to="/demo/dashboard" className="text-muted-foreground hover:text-primary transition-colors">
                  Demonstração
                </Link>
              </li>
              <li>
                <Link to="/login" className="text-muted-foreground hover:text-primary transition-colors">
                  Login
                </Link>
              </li>
              <li>
                <Link to="/signup" className="text-muted-foreground hover:text-primary transition-colors">
                  Cadastro
                </Link>
              </li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold mb-4">Contato</h3>
            <address className="not-italic text-muted-foreground text-sm">
              <p>Av. Paulista, 1000</p>
              <p>São Paulo, SP</p>
              <p>contato@cotai.com.br</p>
              <p>(11) 99999-9999</p>
            </address>
          </div>
        </div>
        
        <div className="border-t border-border mt-8 pt-6 text-center">
          <p className="text-muted-foreground">© 2025 CotAi Licitação Hub. Todos os direitos reservados.</p>
        </div>
      </div>
    </footer>
  );
};

export default FooterSection;
