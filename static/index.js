 // Enhanced form submission with smooth animations
        document.getElementById("uploadForm").addEventListener("submit", function (e) {
            const loadingEl = document.getElementById("loading");
            const submitBtn = document.getElementById("submitBtn");

            loadingEl.style.display = "block";
            loadingEl.style.animation = "fadeInUp 0.5s ease-out";

            submitBtn.disabled = true;
            submitBtn.textContent = "Processing...";
            submitBtn.style.background = "linear-gradient(135deg, #6c757d 0%, #495057 100%)";

            // Scroll to loading section smoothly
            setTimeout(() => {
                loadingEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }, 100);
        });

        // Add hover effects to form elements
        const formInputs = document.querySelectorAll('.form-control');
        formInputs.forEach(input => {
            input.addEventListener('focus', function () {
                this.parentElement.style.transform = 'scale(1.02)';
            });

            input.addEventListener('blur', function () {
                this.parentElement.style.transform = 'scale(1)';
            });
        });

        // Add intersection observer for scroll animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animationPlayState = 'running';
                }
            });
        }, observerOptions);

        // Observe all animated elements
        document.querySelectorAll('.result-card, .recent-card').forEach(el => {
            observer.observe(el);
        });

        // Add dynamic background particle effects
        function createParticle() {
            const particle = document.createElement('div');
            particle.style.cssText = `
          position: fixed;
          width: 4px;
          height: 4px;
          background: radial-gradient(circle, rgba(102,126,234,0.8) 0%, transparent 70%);
          border-radius: 50%;
          pointer-events: none;
          z-index: 1;
          left: ${Math.random() * 100}vw;
          top: 100vh;
          animation: floatUp ${5 + Math.random() * 5}s linear forwards;
        `;

            document.body.appendChild(particle);

            setTimeout(() => {
                particle.remove();
            }, 10000);
        }

        // Create particles periodically
        setInterval(createParticle, 2000);

        // Add CSS for floating particles
        const style = document.createElement('style');
        style.textContent = `
        @keyframes floatUp {
          0% {
            transform: translateY(0) translateX(0) rotate(0deg);
            opacity: 0;
          }
          10% {
            opacity: 1;
          }
          90% {
            opacity: 1;
          }
          100% {
            transform: translateY(-100vh) translateX(${Math.random() * 200 - 100}px) rotate(360deg);
            opacity: 0;
          }
        }
      `;
        document.head.appendChild(style);