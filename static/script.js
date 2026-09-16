// ==========================================
// SUPER YODHA - MAIN JAVASCRIPT
// ==========================================

document.addEventListener("DOMContentLoaded", () => {

    // ==========================================
    // 1. MOBILE MENU
    // ==========================================

    const menuButton = document.querySelector(".menu-toggle");
    const navLinks = document.querySelector(".nav-links");

    if (menuButton && navLinks) {

        menuButton.addEventListener("click", () => {
            navLinks.classList.toggle("active");
        });

        document.querySelectorAll(".nav-links a").forEach(link => {

            link.addEventListener("click", () => {
                navLinks.classList.remove("active");
            });

        });
    }


    // ==========================================
    // 2. SMOOTH SCROLLING
    // ==========================================

    document.querySelectorAll('a[href^="#"]').forEach(link => {

        link.addEventListener("click", function (event) {

            const targetId = this.getAttribute("href");

            if (targetId === "#") {
                return;
            }

            const target = document.querySelector(targetId);

            if (target) {

                event.preventDefault();

                target.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });

            }

        });

    });


    // ==========================================
    // 3. SCROLL REVEAL ANIMATION
    // ==========================================

    const revealElements = document.querySelectorAll(
        ".story-card, .timeline-item, .power-card, .mission-card, .personality-card, .status-card, .guardian-card"
    );

    const revealObserver = new IntersectionObserver(
        (entries) => {

            entries.forEach(entry => {

                if (entry.isIntersecting) {

                    entry.target.classList.add("visible");

                }

            });

        },
        {
            threshold: 0.15
        }
    );


    revealElements.forEach(element => {

        element.classList.add("reveal");

        revealObserver.observe(element);

    });


    // ==========================================
    // 4. POWER CARD INTERACTION
    // ==========================================

    const powerCards =
        document.querySelectorAll(".power-card");


    powerCards.forEach(card => {

        card.addEventListener("click", () => {

            powerCards.forEach(otherCard => {

                if (otherCard !== card) {

                    otherCard.classList.remove(
                        "expanded"
                    );

                }

            });


            card.classList.toggle("expanded");

        });

    });


    // ==========================================
    // 5. MOUSE PARALLAX EFFECT
    // ==========================================

    const heroSection =
        document.querySelector(".hero");


    if (heroSection) {

        heroSection.addEventListener(
            "mousemove",
            (event) => {

                const x =
                    (event.clientX /
                        window.innerWidth - 0.5) * 2;

                const y =
                    (event.clientY /
                        window.innerHeight - 0.5) * 2;


                const heroImage =
                    document.querySelector(
                        ".hero-image"
                    );


                if (heroImage) {

                    heroImage.style.transform =
                        `translate(${x * 8}px, ${y * 8}px)`;

                }

            }
        );


        heroSection.addEventListener(
            "mouseleave",
            () => {

                const heroImage =
                    document.querySelector(
                        ".hero-image"
                    );


                if (heroImage) {

                    heroImage.style.transform =
                        "translate(0, 0)";

                }

            }
        );

    }


    // ==========================================
    // 6. DYNAMIC COSMIC PARTICLES
    // ==========================================

    const particleContainer =
        document.querySelector(
            ".background-effects"
        );


    if (particleContainer) {

        for (let i = 0; i < 35; i++) {

            const particle =
                document.createElement("span");


            particle.classList.add(
                "particle"
            );


            particle.style.left =
                Math.random() * 100 + "%";


            particle.style.top =
                Math.random() * 100 + "%";


            particle.style.animationDelay =
                Math.random() * 5 + "s";


            particle.style.animationDuration =
                5 + Math.random() * 8 + "s";


            particleContainer.appendChild(
                particle
            );

        }

    }


    // ==========================================
    // 7. HERO ENTRANCE ANIMATION
    // ==========================================

    const heroContent =
        document.querySelector(
            ".hero-content"
        );


    const heroImage =
        document.querySelector(
            ".hero-image"
        );


    if (heroContent) {

        heroContent.classList.add(
            "hero-content-enter"
        );

    }


    if (heroImage) {

        heroImage.classList.add(
            "hero-image-enter"
        );

    }


    // ==========================================
    // 8. SUPER YODHA CHATBOT
    // ==========================================

    /*
        IMPORTANT:

        These IDs match your existing
        index.html:

        chatMessages
        chatInput
        sendMessage
    */


    const chatMessages =
        document.querySelector(
            "#chatMessages"
        );


    const chatInput =
        document.querySelector(
            "#chatInput"
        );


    const sendMessage =
        document.querySelector(
            "#sendMessage"
        );


    // ==========================================
    // CHATBOT DATA
    // ==========================================

    let conversationStep = 0;


    let userData = {

        name: "",
        age: "",
        location: "",
        email: "",
        grievance: ""

    };


    // Questions asked by Super Yodha

    const questions = [

        "What is your name?",

        "What is your age?",

        "Where are you located?",

        "What is your email address?",

        "Tell me about the problem you are facing."

    ];


    // ==========================================
    // ADD CHAT MESSAGE
    // ==========================================

    function addMessage(message, sender) {

        if (!chatMessages) {
            return;
        }


        const messageElement =
            document.createElement("div");


        messageElement.classList.add(
            "chat-message",
            sender
        );


        messageElement.textContent =
            message;


        chatMessages.appendChild(
            messageElement
        );


        chatMessages.scrollTop =
            chatMessages.scrollHeight;

    }


    // ==========================================
    // START CHAT
    // ==========================================

    function startChat() {

        conversationStep = 0;


        userData = {

            name: "",
            age: "",
            location: "",
            email: "",
            grievance: ""

        };


        if (chatMessages) {

            chatMessages.innerHTML = "";

        }


        addMessage(
            "Greetings. I am Super Yodha. Tell me what troubles you.",
            "bot"
        );


        setTimeout(() => {

            addMessage(
                questions[0],
                "bot"
            );

        }, 700);

    }


    // ==========================================
    // START CHAT AUTOMATICALLY
    // ==========================================

    if (chatMessages) {

        startChat();

    }


    // ==========================================
    // EMAIL VALIDATION
    // ==========================================

    function isValidEmail(email) {

        const emailPattern =
            /^[^\s@]+@[^\s@]+\.[^\s@]+$/;


        return emailPattern.test(email);

    }


    // ==========================================
    // SEND CHAT MESSAGE
    // ==========================================

    async function handleMessage() {

        if (!chatInput) {
            return;
        }


        const answer =
            chatInput.value.trim();


        // Don't allow empty messages

        if (!answer) {

            return;

        }


        // Show user's message

        addMessage(
            answer,
            "user"
        );


        // Clear input

        chatInput.value = "";


        // ======================================
        // NAME
        // ======================================

        if (conversationStep === 0) {

            userData.name =
                answer;


            conversationStep++;


            setTimeout(() => {

                addMessage(
                    questions[1],
                    "bot"
                );

            }, 500);


            return;

        }


        // ======================================
        // AGE
        // ======================================

        if (conversationStep === 1) {

            if (!/^\d+$/.test(answer)) {

                addMessage(
                    "Please enter your age using numbers.",
                    "bot"
                );

                return;

            }


            userData.age =
                answer;


            conversationStep++;


            setTimeout(() => {

                addMessage(
                    questions[2],
                    "bot"
                );

            }, 500);


            return;

        }


        // ======================================
        // LOCATION
        // ======================================

        if (conversationStep === 2) {

            userData.location =
                answer;


            conversationStep++;


            setTimeout(() => {

                addMessage(
                    questions[3],
                    "bot"
                );

            }, 500);


            return;

        }


        // ======================================
        // EMAIL
        // ======================================

        if (conversationStep === 3) {

            if (!isValidEmail(answer)) {

                addMessage(
                    "That email address doesn't look valid. Please enter a valid email.",
                    "bot"
                );

                return;

            }


            userData.email =
                answer;


            conversationStep++;


            setTimeout(() => {

                addMessage(
                    questions[4],
                    "bot"
                );

            }, 500);


            return;

        }


        // ======================================
        // GRIEVANCE
        // ======================================

        if (conversationStep === 4) {

            userData.grievance =
                answer;


            addMessage(
                "Your request is being recorded...",
                "bot"
            );


            await submitRequest();

        }

    }


    // ==========================================
    // CONNECT SEND BUTTON
    // ==========================================

    if (sendMessage) {

        sendMessage.addEventListener(
            "click",
            handleMessage
        );

    }


    // ==========================================
    // ENTER KEY SUPPORT
    // ==========================================

    if (chatInput) {

        chatInput.addEventListener(
            "keydown",
            (event) => {

                if (event.key === "Enter") {

                    event.preventDefault();

                    handleMessage();

                }

            }
        );

    }


    // ==========================================
    // SUBMIT REQUEST TO FLASK
    // ==========================================

    async function submitRequest() {

        try {

            const response =
                await fetch(
                    "/submit",
                    {

                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(
                                userData
                            )

                    }
                );


            const result =
                await response.json();


            // ==================================
            // SUCCESS
            // ==================================

            if (result.success) {

                addMessage(
                    "Your request has been received.",
                    "bot"
                );


                addMessage(
                    `Your request ID is #${result.request_id}.`,
                    "bot"
                );


                addMessage(
                    "Your request has been recorded and will be reviewed.",
                    "bot"
                );


                conversationStep = 5;

            }


            // ==================================
            // ERROR
            // ==================================

            else {

                addMessage(
                    result.message ||
                    "Something went wrong. Please try again.",
                    "bot"
                );

            }

        }


        catch (error) {

            console.error(
                "Submission error:",
                error
            );


            addMessage(
                "Unable to connect to Super Yodha's system. Please try again.",
                "bot"
            );

        }

    }

});