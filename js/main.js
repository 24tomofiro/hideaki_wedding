document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Particles.js
    particlesJS('particles-js', {
        "particles": {
            "number": {
                "value": 80,
                "density": {
                    "enable": true,
                    "value_area": 800
                }
            },
            "color": {
                "value": "#f2d06b"
            },
            "shape": {
                "type": "circle",
                "stroke": {
                    "width": 0,
                    "color": "#000000"
                },
                "polygon": {
                    "nb_sides": 5
                }
            },
            "opacity": {
                "value": 0.5,
                "random": false,
                "anim": {
                    "enable": false,
                    "speed": 1,
                    "opacity_min": 0.1,
                    "sync": false
                }
            },
            "size": {
                "value": 3,
                "random": true,
                "anim": {
                    "enable": false,
                    "speed": 40,
                    "size_min": 0.1,
                    "sync": false
                }
            },
            "line_linked": {
                "enable": true,
                "distance": 150,
                "color": "#ffffff",
                "opacity": 0.2,
                "width": 1
            },
            "move": {
                "enable": true,
                "speed": 2,
                "direction": "none",
                "random": false,
                "straight": false,
                "out_mode": "out",
                "bounce": false,
                "attract": {
                    "enable": false,
                    "rotateX": 600,
                    "rotateY": 1200
                }
            }
        },
        "interactivity": {
            "detect_on": "canvas",
            "events": {
                "onhover": {
                    "enable": true,
                    "mode": "grab"
                },
                "onclick": {
                    "enable": true,
                    "mode": "push"
                },
                "resize": true
            },
            "modes": {
                "grab": {
                    "distance": 140,
                    "line_linked": {
                        "opacity": 1
                    }
                },
                "bubble": {
                    "distance": 400,
                    "size": 40,
                    "duration": 2,
                    "opacity": 8,
                    "speed": 3
                },
                "repulse": {
                    "distance": 200,
                    "duration": 0.4
                },
                "push": {
                    "particles_nb": 4
                },
                "remove": {
                    "particles_nb": 2
                }
            }
        },
        "retina_detect": true
    });

    // 1.5 Load Hero Slideshow
    const heroSlideshow = document.getElementById('hero-slideshow');
    const slideshowImages = [
        "2013-12-31 10.38.41.jpg",
        "DSC02878.JPG",
        "GRL_0068.JPG",
        "KC3R0017.JPG",
        "LINE_ALBUM_20241022_260228_1.jpg",
        "LINE_ALBUM_20241022_260228_10.jpg"
    ];

    if (heroSlideshow) {
        let currentSlide = 0;
        const slides = [];

        slideshowImages.forEach((file, index) => {
            const slide = document.createElement('div');
            slide.className = 'slideshow-slide' + (index === 0 ? ' active' : '');
            slide.style.backgroundImage = `url('assets/${file}')`;
            heroSlideshow.appendChild(slide);
            slides.push(slide);
        });

        if (slides.length > 1) {
            setInterval(() => {
                slides[currentSlide].classList.remove('active');
                currentSlide = (currentSlide + 1) % slides.length;
                slides[currentSlide].classList.add('active');
            }, 6000); // Change image every 6 seconds
        }
    }

    // 2. Load Gallery Images
    const galleryContainer = document.getElementById('gallery-container');
    // List of images from the assets folder. In a real app with a backend, we might fetch this list.
    // Since this is static, we hardcode the known filenames.
    const imageFiles = [
        "2013-12-31 10.38.41.jpg",
        "DSC02878.JPG",
        "GRL_0068.JPG",
        "KC3R0017.JPG",
        "LINE_ALBUM_20241022_260228_1.jpg",
        "LINE_ALBUM_20241022_260228_2.jpg",
        "LINE_ALBUM_20241022_260228_3.jpg",
        "LINE_ALBUM_20241022_260228_4.jpg",
        "LINE_ALBUM_20241022_260228_6.jpg",
        "LINE_ALBUM_20241022_260228_7.jpg",
        "LINE_ALBUM_20241022_260228_8.jpg",
        "LINE_ALBUM_20241022_260228_9.jpg",
        "LINE_ALBUM_20241022_260228_10.jpg"
    ];

    imageFiles.forEach((file, index) => {
        const item = document.createElement('div');
        item.className = 'gallery-item reveal';
        // Add staggered delay for nice load effect
        item.style.transitionDelay = `${(index % 4) * 0.1}s`;

        const img = document.createElement('img');
        img.src = `assets/${file}`;
        img.alt = `Memory ${index + 1}`;
        // Basic error handling in case a file is missing
        img.onerror = () => { item.style.display = 'none'; };

        item.appendChild(img);
        galleryContainer.appendChild(item);
    });


    // 3. Scroll Reveal Animation Logic
    function reveal() {
        const reveals = document.querySelectorAll(".reveal");
        for (let i = 0; i < reveals.length; i++) {
            const windowHeight = window.innerHeight;
            const elementTop = reveals[i].getBoundingClientRect().top;
            const elementVisible = 100; // when to trigger

            if (elementTop < windowHeight - elementVisible) {
                reveals[i].classList.add("active");
            }
        }
    }

    // Trigger reveal on scroll and initial load
    window.addEventListener("scroll", reveal);
    reveal();
});
