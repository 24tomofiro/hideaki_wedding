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

    // 2. Scroll Reveal Animation Logic
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

    // 3. YouTube Autoplay on Scroll Logic
    const specialMovieWrapper = document.querySelector('#special-movie .video-wrapper');
    const specialMovieIframe = document.getElementById('special-movie-iframe');

    if (specialMovieWrapper && specialMovieIframe) {
        let isVideoPlaying = false;

        const videoObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    if (!isVideoPlaying) {
                        // Play video via YouTube API postMessage
                        specialMovieIframe.contentWindow.postMessage('{"event":"command","func":"playVideo","args":""}', '*');
                        isVideoPlaying = true;
                    }
                } else {
                    if (isVideoPlaying) {
                        // Pause video when out of view
                        specialMovieIframe.contentWindow.postMessage('{"event":"command","func":"pauseVideo","args":""}', '*');
                        isVideoPlaying = false;
                    }
                }
            });
        }, { threshold: 0.3 }); // Trigger when 30% of the video is visible

        videoObserver.observe(specialMovieWrapper);
    }
});
