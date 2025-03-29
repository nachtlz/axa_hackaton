<template>
    <footer class="footer">
      <!-- Sección principal del footer -->
      <div class="footer-main">
        <div class="footer-section">
          <h3>SOBRE NOSOTROS</h3>
          <ul>
            <li><a href="#">Encuentra tu oficina</a></li>
            <li><a href="#">Blogs AXA</a></li>
            <li><a href="#">Únete a nuestro equipo</a></li>
          </ul>
        </div>
  
        <div class="footer-section">
          <h3>APPS PARA MÓVILES</h3>
          <ul>
            <li><a href="#">App My AXA</a></li>
            <li><a href="#">App Vida Ahorro</a></li>
          </ul>
        </div>
  
        <div class="footer-section">
          <h3>PROMOCIONES</h3>
          <ul>
            <li><a href="#">Promociones</a></li>
            <li><a href="#">Club de ventajas</a></li>
          </ul>
        </div>
  
        <div class="footer-section">
          <h3>ACCESOS PROFESIONALES</h3>
          <ul>
            <li><a href="#">Acceso para agentes</a></li>
            <li><a href="#">Acceso para proveedores</a></li>
          </ul>
  
          <div class="social-media">
            <h3>SÍGUENOS:</h3>
            <div class="social-icons">
              <a href="#" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
              <a href="#" aria-label="Twitter"><i class="fab fa-x-twitter"></i></a>
              <a href="#" aria-label="YouTube"><i class="fab fa-youtube"></i></a>
              <a href="#" aria-label="LinkedIn"><i class="fab fa-linkedin-in"></i></a>
              <a href="#" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
              <a href="#" aria-label="TikTok"><i class="fab fa-tiktok"></i></a>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Sección inferior del footer -->
      <div class="footer-bottom">
        <div class="legal-links">
          <a href="#">Sitemap</a>
          <a href="#">Información legal</a>
          <a href="#">Cookies</a>
          <a href="#">Política de privacidad</a>
          <a href="#">Accesibilidad</a>
          <a href="#">Normas de uso de RRSS</a>
          <span class="copyright">Copyright AXA 2025 ©</span>
        </div>
        
       
      </div>
    </footer>
  </template>
  
  <script setup>
  // No se necesitan props o datos adicionales para este componente estático
  </script>
  
  <style scoped>
  .footer {
    font-family: Arial, sans-serif;
    color: white;
    background-color: #4a7ab8;
    padding: 0;
    width: 100%;
  }
  
  .footer-main {
    display: flex;
    justify-content: space-between;
    padding: 2rem 4rem;
    flex-wrap: wrap;
  }
  
  .footer-section {
    flex: 1;
    min-width: 200px;
    margin-bottom: 1.5rem;
  }
  
  h3 {
    font-size: 1rem;
    font-weight: bold;
    margin-bottom: 1rem;
  }
  
  ul {
    list-style-type: none;
    padding: 0;
    margin: 0;
  }
  
  li {
    margin-bottom: 0.75rem;
  }
  
  a {
    color: white;
    text-decoration: none;
    font-size: 0.95rem;
  }
  
  a:hover {
    text-decoration: underline;
  }
  
  .social-media {
    margin-top: 2rem;
  }
  
  .social-icons {
    display: flex;
    gap: 1rem;
  }
  
  .social-icons a {
    font-size: 1.2rem;
  }
  
  .footer-bottom {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 4rem;
    border-top: 1px solid rgba(255, 255, 255, 0.2);
    position: relative;
  }
  
  .legal-links {
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem;
    font-size: 0.85rem;
  }
  
  .copyright {
    color: white;
    font-size: 0.85rem;
  }
  
  .accessibility-button {
    position: absolute;
    left: 3rem;
    bottom: 1rem;
    background-color: #00039c;
    color: white;
    border: none;
    border-radius: 50%;
    width: 3.5rem;
    height: 3.5rem;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
  }
  
  .accessibility-icon {
    font-size: 1.5rem;
  }
  
  @media (max-width: 768px) {
    .footer-main {
      flex-direction: column;
      padding: 2rem;
    }
    
    .footer-bottom {
      flex-direction: column;
      gap: 1rem;
      padding: 1rem 2rem;
    }
    
    .legal-links {
      flex-direction: column;
      align-items: center;
      gap: 0.75rem;
    }
    
    .accessibility-button {
      position: fixed;
      left: 1rem;
      bottom: 1rem;
    }
  }
  </style>