/**
 * რა? სად? როდის? — ინტელექტ-კლუბის კლიენტი
 * Features: 6 მოაზროვნე (კაპიტანი, მათემატიკა, გეოგრაფია, ბიოლოგია, ისტორია, სპორტი), 1 წუთი ფიქრისთვის, ბროლის ბუ ქვიზი
 */

// ==========================================
// 1. STATE & LOCALIZATION DICTIONARY
// ==========================================
const state = {
    lang: localStorage.getItem('ra_lang') || 'ka',
    soundEnabled: localStorage.getItem('ra_sound') !== 'false',
    activeTab: 'chat',
    activeAgent: 'auto',
    sessionId: localStorage.getItem('ra_sess') || ('sess_' + Math.random().toString(36).substring(2, 10)),
    quiz: {
        score: parseInt(localStorage.getItem('ra_quiz_score') || '0', 10),
        streak: parseInt(localStorage.getItem('ra_quiz_streak') || '0', 10),
        current: null,
        answered: false,
        subject: 'mixed'
    },
    agentsMeta: {}
};

localStorage.setItem('ra_sess', state.sessionId);

const i18n = {
    ka: {
        tab_chat: "მოაზროვნეები",
        tab_syndicate: "1 წუთი ფიქრისთვის",
        tab_quiz: "ბროლის ბუ",
        tab_dossier: "გუნდის შემადგენლობა",
        status_online: "თამაში აქტიურია",
        agent_auto_name: "ჭკვიანი შერჩევა",
        agent_auto_desc: "თემის მიხედვით",
        agent_leader_name: "ალექსი (კაპიტანი)",
        agent_leader_role: "სტრატეგი & სინთეზი",
        agent_math_name: "თეა (მათემატიკა)",
        agent_math_role: "ლოგიკა & რიცხვები",
        agent_geo_name: "სანდრო (გეოგრაფია)",
        agent_geo_role: "რუკა & ქვეყნები",
        agent_bio_name: "ლუკა (ბიოლოგია)",
        agent_bio_role: "ფლორა & ფაუნა",
        agent_hist_name: "ნინო (ისტორია)",
        agent_hist_role: "ეპოქები & ფაქტები",
        agent_sport_name: "დავითი (სპორტი)",
        agent_sport_role: "ოლიმპიადა & რეკორდები",
        btn_clear_history: "ისტორიის გასუფთავება",
        sample_prompts_title: "სცადეთ ერთ-ერთი შეკითხვა:",
        btn_send: "გაგზავნა",
        chat_placeholder: "დასვით შეკითხვა მოაზროვნეებთან (გეოგრაფია, სპორტი, ისტორია, ბიოლოგია, მათემატიკა)...",
        syndicate_title: "გუნდური განხილვის მაგიდა",
        syndicate_desc: "დასვით ინტელექტუალური შეკითხვა. გუნდის კაპიტანი გამოაცხადებს 1 წუთს ფიქრისთვის — 5-ვე ექსპერტი (მათემატიკა, გეოგრაფია, ბიოლოგია, ისტორია, სპორტი) წამოაყენებს თავის ვერსიას, დასასრულს კი კაპიტანი ჩამოაყალიბებს გუნდის ოფიციალურ პასუხს!",
        syndicate_presets: "რეკომენდებული ინტელექტუალური შეკითხვები:",
        btn_start_syndicate: "1 წუთის დაწყება",
        syndicate_placeholder: "ჩაწერეთ შეკითხვა 1 წუთიანი გუნდური განხილვისთვის...",
        syndicate_empty_title: "მზადება 1 წუთიანი განხილვისთვის",
        syndicate_empty_desc: "შეიყვანეთ შეკითხვა და იხილეთ, როგორ განიხილავენ კაპიტანი, თეა, სანდრო, ლუკა, ნინო და დავითი ვერსიებს რეალურ დროში.",
        quiz_score: "ქულა",
        quiz_streak: "სერია",
        subj_mixed: "სუპერ-რაუნდი",
        subj_geo: "გეოგრაფია",
        subj_sport: "სპორტი",
        subj_hist: "ისტორია",
        subj_bio: "ბიოლოგია",
        subj_math: "მათემატიკა",
        btn_next_question: "შემდეგი შეკითხვა",
        thinking: "მოაზროვნე აანალიზებს...",
        copied: "ტექსტი დაკოპირდა!",
        toast_reset: "ჩატის ისტორია გასუფთავდა",
        correct_title: "სწორია! ბროლის ბუს რაუნდი მოგებულია! 🦉🎉",
        wrong_title: "არასწორია! სწორი პასუხი მონიშნულია მწვანედ."
    },
    en: {
        tab_chat: "Thinkers",
        tab_syndicate: "1 Minute to Think",
        tab_quiz: "Crystal Owl",
        tab_dossier: "Club Roster",
        status_online: "Game Active",
        agent_auto_name: "Smart Dispatch",
        agent_auto_desc: "By subject",
        agent_leader_name: "Alex (Captain)",
        agent_leader_role: "Strategist & Synthesis",
        agent_math_name: "Tea (Math)",
        agent_math_role: "Logic & Numbers",
        agent_geo_name: "Sandro (Geography)",
        agent_geo_role: "Maps & Exploration",
        agent_bio_name: "Luka (Biology)",
        agent_bio_role: "Flora & Fauna",
        agent_hist_name: "Nino (History)",
        agent_hist_role: "Epochs & Civilizations",
        agent_sport_name: "David (Sport)",
        agent_sport_role: "Olympics & Records",
        btn_clear_history: "Clear History",
        sample_prompts_title: "Try one of these questions:",
        btn_send: "Send",
        chat_placeholder: "Ask the team a question (Geography, Sport, History, Biology, Math)...",
        syndicate_title: "Roundtable Brainstorm Chamber",
        syndicate_desc: "Ask an intellectual question. The Captain starts the 1-minute countdown — all 5 specialists (Math, Geography, Biology, History, Sport) offer clues, and the Captain formulates the official team answer!",
        syndicate_presets: "Recommended Intellectual Questions:",
        btn_start_syndicate: "Start 1 Minute",
        syndicate_placeholder: "Enter an intellectual riddle for the 1-minute round...",
        syndicate_empty_title: "Awaiting 1-Minute Challenge",
        syndicate_empty_desc: "Enter a question to observe Captain Alex, Tea, Sandro, Luka, Nino, and David brainstorm.",
        quiz_score: "Score",
        quiz_streak: "Streak",
        subj_mixed: "Super Round",
        subj_geo: "Geography",
        subj_sport: "Sport",
        subj_hist: "History",
        subj_bio: "Biology",
        subj_math: "Mathematics",
        btn_next_question: "Next Question",
        thinking: "Thinker deliberating...",
        copied: "Copied to clipboard!",
        toast_reset: "History cleared",
        correct_title: "Correct! The Crystal Owl round is won! 🦉🎉",
        wrong_title: "Incorrect! Correct answer highlighted in emerald."
    }
};

// ==========================================
// 2. WEB AUDIO SYNTHESIZER
// ==========================================
let audioCtx = null;

function getAudioContext() {
    if (!audioCtx) {
        const AudioContextClass = window.AudioContext || window.webkitAudioContext;
        if (AudioContextClass) {
            audioCtx = new AudioContextClass();
        }
    }
    if (audioCtx && audioCtx.state === 'suspended') {
        audioCtx.resume();
    }
    return audioCtx;
}

function playTone(freq, type = 'sine', duration = 0.15, gainVal = 0.08) {
    if (!state.soundEnabled) return;
    try {
        const ctx = getAudioContext();
        if (!ctx) return;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, ctx.currentTime);
        gain.gain.setValueAtTime(gainVal, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + duration);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + duration);
    } catch (e) {}
}

function playSendSound() {
    playTone(560, 'sine', 0.1, 0.05);
}

function playChimeSound() {
    if (!state.soundEnabled) return;
    try {
        const ctx = getAudioContext();
        if (!ctx) return;
        const notes = [659.25, 880, 1046.5];
        notes.forEach((freq, idx) => {
            setTimeout(() => {
                playTone(freq, 'sine', 0.25, 0.04);
            }, idx * 70);
        });
    } catch (e) {}
}

function playGongSound() {
    if (!state.soundEnabled) return;
    try {
        const ctx = getAudioContext();
        if (!ctx) return;
        // Deep gong sound for "რა? სად? როდის?" 1 minute start
        playTone(261.63, 'triangle', 0.8, 0.12);
        setTimeout(() => playTone(392.00, 'sine', 0.7, 0.08), 80);
    } catch (e) {}
}

function playCorrectSound() {
    if (!state.soundEnabled) return;
    try {
        const ctx = getAudioContext();
        if (!ctx) return;
        const chord = [523.25, 659.25, 783.99, 1046.5];
        chord.forEach((freq, idx) => {
            setTimeout(() => {
                playTone(freq, 'triangle', 0.35, 0.06);
            }, idx * 60);
        });
    } catch (e) {}
}

function playWrongSound() {
    playTone(220, 'sawtooth', 0.25, 0.05);
}

// ==========================================
// 3. BACKGROUND NEURAL CONSTELLATION CANVAS
// ==========================================
function initNeuralCanvas() {
    const canvas = document.getElementById('neuralCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let width = canvas.width = window.innerWidth;
    let height = canvas.height = window.innerHeight;

    window.addEventListener('resize', () => {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    });

    const particles = [];
    const count = Math.min(Math.floor((width * height) / 16000), 85);

    for (let i = 0; i < count; i++) {
        particles.push({
            x: Math.random() * width,
            y: Math.random() * height,
            vx: (Math.random() - 0.5) * 0.5,
            vy: (Math.random() - 0.5) * 0.5,
            radius: Math.random() * 2 + 1,
            hue: [45, 195, 155, 25][Math.floor(Math.random() * 4)] // Golden and blue hues
        });
    }

    let mouse = { x: -1000, y: -1000 };
    window.addEventListener('mousemove', (e) => {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
    });

    function draw() {
        ctx.clearRect(0, 0, width, height);

        for (let i = 0; i < particles.length; i++) {
            const p = particles[i];
            p.x += p.vx;
            p.y += p.vy;

            if (p.x < 0) p.x = width;
            if (p.x > width) p.x = 0;
            if (p.y < 0) p.y = height;
            if (p.y > height) p.y = 0;

            const dxm = p.x - mouse.x;
            const dym = p.y - mouse.y;
            const distM = Math.sqrt(dxm * dxm + dym * dym);
            if (distM < 130) {
                p.x += (dxm / distM) * 0.9;
                p.y += (dym / distM) * 0.9;
            }

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fillStyle = `hsla(${p.hue}, 85%, 65%, 0.7)`;
            ctx.fill();

            for (let j = i + 1; j < particles.length; j++) {
                const p2 = particles[j];
                const dx = p.x - p2.x;
                const dy = p.y - p2.y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < 135) {
                    ctx.beginPath();
                    ctx.moveTo(p.x, p.y);
                    ctx.lineTo(p2.x, p2.y);
                    const alpha = (1 - dist / 135) * 0.25;
                    ctx.strokeStyle = `rgba(245, 158, 11, ${alpha})`;
                    ctx.lineWidth = 0.85;
                    ctx.stroke();
                }
            }
        }

        requestAnimationFrame(draw);
    }

    draw();
}

// ==========================================
// 4. CONFETTI CELEBRATION PHYSICS
// ==========================================
let confettiParticles = [];
let confettiAnimationId = null;

function launchConfetti() {
    const canvas = document.getElementById('confettiCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    confettiParticles = [];
    const colors = ['#f59e0b', '#fbbf24', '#0ea5e9', '#10b981', '#f43f5e', '#f97316', '#38bdf8'];

    for (let i = 0; i < 95; i++) {
        confettiParticles.push({
            x: canvas.width / 2 + (Math.random() - 0.5) * 200,
            y: canvas.height * 0.4 + (Math.random() - 0.5) * 100,
            vx: (Math.random() - 0.5) * 16,
            vy: -Math.random() * 12 - 4,
            size: Math.random() * 7 + 4,
            color: colors[Math.floor(Math.random() * colors.length)],
            rotation: Math.random() * 360,
            rotSpeed: (Math.random() - 0.5) * 12,
            opacity: 1,
            gravity: 0.35
        });
    }

    if (confettiAnimationId) cancelAnimationFrame(confettiAnimationId);

    function updateConfetti() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        let active = false;

        for (let i = 0; i < confettiParticles.length; i++) {
            const p = confettiParticles[i];
            p.x += p.vx;
            p.y += p.vy;
            p.vy += p.gravity;
            p.vx *= 0.98;
            p.rotation += p.rotSpeed;
            p.opacity -= 0.008;

            if (p.opacity > 0) {
                active = true;
                ctx.save();
                ctx.translate(p.x, p.y);
                ctx.rotate((p.rotation * Math.PI) / 180);
                ctx.fillStyle = p.color;
                ctx.globalAlpha = Math.max(0, p.opacity);
                ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 1.4);
                ctx.restore();
            }
        }

        if (active) {
            confettiAnimationId = requestAnimationFrame(updateConfetti);
        } else {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        }
    }

    updateConfetti();
}

// ==========================================
// 5. 3D CARD TILT INTERACTION
// ==========================================
function init3DTiltCards() {
    document.querySelectorAll('.tilt-card').forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = ((y - centerY) / centerY) * -6;
            const rotateY = ((x - centerX) / centerX) * 6;

            card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) translateY(-3px)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0px)';
        });
    });
}

// ==========================================
// 6. UI LOCALIZATION
// ==========================================
function updateLanguageUI() {
    const lang = state.lang;
    const texts = i18n[lang];

    document.documentElement.lang = lang;
    const langCodeEl = document.getElementById('langCode');
    if (langCodeEl) langCodeEl.textContent = lang === 'ka' ? 'GE' : 'EN';

    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (texts[key]) {
            el.textContent = texts[key];
        }
    });

    const chatInput = document.getElementById('chatInput');
    if (chatInput) chatInput.placeholder = texts.chat_placeholder;

    const syndicateInput = document.getElementById('syndicateInput');
    if (syndicateInput) syndicateInput.placeholder = texts.syndicate_placeholder;

    updateActiveAgentBanner();
    renderQuickPills();
    updateQuizStatsDisplay();
}

function toggleLanguage() {
    state.lang = state.lang === 'ka' ? 'en' : 'ka';
    localStorage.setItem('ra_lang', state.lang);
    updateLanguageUI();
    showToast(state.lang === 'ka' ? "ენა შეიცვალა: ქართული" : "Language switched: English");
}

function showToast(message) {
    const container = document.getElementById('toastContainer');
    if (!container) return;
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(12px) scale(0.95)';
        setTimeout(() => toast.remove(), 300);
    }, 2800);
}

// ==========================================
// 7. MARKDOWN FORMATTER
// ==========================================
function formatMarkdown(text) {
    if (!text) return '';
    let escaped = text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');

    escaped = escaped.replace(/```([a-zA-Z]*)\n([\s\S]*?)```/g, (match, lang, code) => {
        return `<pre><code>${code.trim()}</code></pre>`;
    });

    escaped = escaped.replace(/`([^`]+)`/g, '<code>$1</code>');
    escaped = escaped.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    escaped = escaped.replace(/\*([^*]+)\*/g, '<em>$1</em>');
    escaped = escaped.replace(/^### (.*$)/gim, '<h4 style="margin: 0.5rem 0; font-weight:700;">$1</h4>');
    escaped = escaped.replace(/^## (.*$)/gim, '<h3 style="margin: 0.6rem 0; font-weight:700;">$1</h3>');

    escaped = escaped.replace(/^\s*[-*]\s+(.*)$/gim, '<li>$1</li>');
    escaped = escaped.replace(/(<li>[\s\S]*?<\/li>)/gm, '<ul>$1</ul>');
    escaped = escaped.replace(/<\/ul>\s*<ul>/gm, '');

    const paragraphs = escaped.split(/\n\s*\n/);
    return paragraphs.map(p => {
        p = p.trim();
        if (!p) return '';
        if (p.startsWith('<pre>') || p.startsWith('<ul>') || p.startsWith('<h')) {
            return p;
        }
        return `<p>${p.replace(/\n/g, '<br>')}</p>`;
    }).join('');
}

// ==========================================
// 8. AGENT METADATA & QUICK PROMPTS
// ==========================================
async function fetchAgentsMetadata() {
    try {
        const res = await fetch('/api/agents');
        const data = await res.json();
        if (data.success && data.agents) {
            data.agents.forEach(a => {
                state.agentsMeta[a.id] = a;
            });
            renderQuickPills();
            updateActiveAgentBanner();
            init3DTiltCards();
        }
    } catch (e) {
        console.warn('Could not fetch agents metadata:', e);
    }
}

function updateActiveAgentBanner() {
    const avatarEl = document.getElementById('activeAvatar');
    const nameEl = document.getElementById('activeName');
    const badgeEl = document.getElementById('activeBadge');
    const descEl = document.getElementById('activeDesc');

    const agentId = state.activeAgent;
    const isKa = state.lang === 'ka';

    if (agentId === 'auto') {
        if (avatarEl) avatarEl.textContent = '🤖';
        if (nameEl) nameEl.textContent = isKa ? 'ჭკვიანი შერჩევა (Auto-Select)' : 'Smart Dispatch (Auto-Select)';
        if (badgeEl) badgeEl.textContent = 'რა? სად? როდის?';
        if (descEl) descEl.textContent = isKa 
            ? 'სისტემა ავტომატურად გააანალიზებს თქვენს კითხვას და გადასცემს შესაბამის მოაზროვნეს.'
            : 'The system inspects query intent and dispatches to the most specialized thinker.';
        return;
    }

    const agent = state.agentsMeta[agentId];
    if (agent) {
        if (avatarEl) avatarEl.textContent = agent.avatar;
        if (nameEl) nameEl.textContent = agent.name;
        if (badgeEl) badgeEl.textContent = agent.badge;
        if (descEl) descEl.textContent = isKa ? agent.specialty_ka : agent.specialty;
    }
}

function renderQuickPills() {
    const pillsRow = document.getElementById('quickPillsRow');
    if (!pillsRow) return;
    pillsRow.innerHTML = '';

    const agentId = state.activeAgent;
    const isKa = state.lang === 'ka';

    let prompts = [];
    if (agentId === 'auto' || !state.agentsMeta[agentId]) {
        prompts = [
            isKa ? "რომელია მსოფლიოში ერთადერთი ზღვა სანაპიროს გარეშე?" : "Which sea has no land coastline?",
            isKa ? "მომიყევი დინამო თბილისის 1981 წლის ევროპის თასის ტრიუმფზე." : "Tell me about Dinamo Tbilisi winning the 1981 European Cup.",
            isKa ? "რომელ წელს მოხდა დიდგორის ბრძოლა და რატომ ეწოდა 'ძლევაი საკვირველი'?" : "Tell me about the Battle of Didgori in 1121.",
            isKa ? "რა არის ეილერის ფორმულა e^(iπ) + 1 = 0?" : "Explain Euler's formula e^(iπ) + 1 = 0.",
            isKa ? "რომელ ცხოველს აქვს ყველაზე უჩვეულო ბიოლოგიური თვისება?" : "Which animal has the most unusual biological adaptation?"
        ];
    } else {
        const agent = state.agentsMeta[agentId];
        if (agent.sample_prompts) {
            prompts = agent.sample_prompts.map(p => isKa ? p.ka : p.en);
        }
    }

    prompts.forEach(promptText => {
        const btn = document.createElement('button');
        btn.className = 'quick-pill hover-lift';
        btn.textContent = promptText;
        btn.addEventListener('click', () => {
            const chatInput = document.getElementById('chatInput');
            if (chatInput) {
                chatInput.value = promptText;
                chatInput.focus();
                submitChatMessage();
            }
        });
        pillsRow.appendChild(btn);
    });
}

// ==========================================
// 9. CHAT LOGIC WITH TYPEWRITER EFFECT
// ==========================================
async function submitChatMessage() {
    const input = document.getElementById('chatInput');
    const list = document.getElementById('chatList');
    if (!input || !list) return;

    const message = input.value.trim();
    if (!message) return;

    input.value = '';
    input.style.height = 'auto';

    const welcomeCard = document.getElementById('welcomeCard');
    if (welcomeCard) welcomeCard.style.display = 'none';

    appendUserMessage(message);
    playSendSound();

    const typingId = 'typing_' + Date.now();
    appendTypingIndicator(typingId);
    scrollChatToBottom();

    try {
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                agent: state.activeAgent,
                sessionId: state.sessionId
            })
        });

        const data = await res.json();
        removeTypingIndicator(typingId);

        if (data.success) {
            appendAgentMessageWithTypewriter(data.agent, data.agent_meta, data.response);
            playChimeSound();
        } else {
            appendErrorMessage(data.error || 'Server error occurred');
        }
    } catch (err) {
        removeTypingIndicator(typingId);
        appendErrorMessage('ქსელის შეცდომა: ვერ მოხერხდა სერვერთან დაკავშირება.');
    }

    scrollChatToBottom();
}

function appendUserMessage(text) {
    const list = document.getElementById('chatList');
    const row = document.createElement('div');
    row.className = 'chat-msg-row user';

    row.innerHTML = `
        <div class="msg-body-wrapper">
            <div class="msg-sender-info">
                <span class="msg-sender-name">${state.lang === 'ka' ? 'თქვენ' : 'You'}</span>
                <span>${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
            </div>
            <div class="msg-bubble">${formatMarkdown(text)}</div>
        </div>
        <div class="msg-avatar float-anim" style="background: rgba(217, 119, 6, 0.25); border-color: #f59e0b;">👤</div>
    `;
    list.appendChild(row);
}

function appendAgentMessageWithTypewriter(agentId, meta, responseText) {
    const list = document.getElementById('chatList');
    const row = document.createElement('div');
    row.className = `chat-msg-row agent agent-${agentId}`;

    const agentMeta = state.agentsMeta[agentId] || meta || {
        name: agentId.toUpperCase(),
        avatar: '🦉',
        color: '#f59e0b'
    };

    const bubbleId = 'bubble_' + Date.now();

    row.innerHTML = `
        <div class="msg-avatar float-anim" style="border-color: ${agentMeta.color}; box-shadow: 0 0 16px ${agentMeta.color}50;">
            ${agentMeta.avatar}
        </div>
        <div class="msg-body-wrapper">
            <div class="msg-sender-info">
                <span class="msg-sender-name" style="color: ${agentMeta.color};">${agentMeta.name}</span>
                <span>${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
            </div>
            <div class="msg-bubble typewriter-cursor" id="${bubbleId}"></div>
            <div class="msg-actions" style="opacity: 0; transition: opacity 0.4s ease;">
                <button class="msg-action-btn btn-copy" data-text="${encodeURIComponent(responseText)}" title="Copy">
                    <span>📋</span> <span>${state.lang === 'ka' ? 'კოპირება' : 'Copy'}</span>
                </button>
                <button class="msg-action-btn btn-speak" data-text="${encodeURIComponent(responseText)}" title="Listen">
                    <span>🔊</span> <span>${state.lang === 'ka' ? 'მოსმენა' : 'Listen'}</span>
                </button>
            </div>
        </div>
    `;

    list.appendChild(row);
    const bubbleEl = row.querySelector(`#${bubbleId}`);
    const actionsEl = row.querySelector('.msg-actions');

    let idx = 0;
    const speed = Math.max(8, Math.min(22, 1400 / responseText.length));
    const stepSize = responseText.length > 400 ? 4 : 2;

    function typeNext() {
        if (idx < responseText.length) {
            idx += stepSize;
            bubbleEl.innerHTML = formatMarkdown(responseText.substring(0, idx));
            scrollChatToBottom();
            setTimeout(typeNext, speed);
        } else {
            bubbleEl.innerHTML = formatMarkdown(responseText);
            bubbleEl.classList.remove('typewriter-cursor');
            if (actionsEl) actionsEl.style.opacity = '1';
            scrollChatToBottom();
        }
    }

    typeNext();

    row.querySelector('.btn-copy').addEventListener('click', (e) => {
        const raw = decodeURIComponent(e.currentTarget.getAttribute('data-text'));
        navigator.clipboard.writeText(raw);
        showToast(state.lang === 'ka' ? i18n.ka.copied : i18n.en.copied);
    });

    row.querySelector('.btn-speak').addEventListener('click', (e) => {
        const raw = decodeURIComponent(e.currentTarget.getAttribute('data-text'));
        speakText(raw);
    });
}

function appendTypingIndicator(id) {
    const list = document.getElementById('chatList');
    const row = document.createElement('div');
    row.className = 'chat-msg-row agent';
    row.id = id;

    row.innerHTML = `
        <div class="msg-avatar">🦉</div>
        <div class="typing-bubble">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <span style="font-size:0.75rem; color: var(--text-muted); margin-left: 0.4rem;">
                ${state.lang === 'ka' ? i18n.ka.thinking : i18n.en.thinking}
            </span>
        </div>
    `;
    list.appendChild(row);
}

function removeTypingIndicator(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

function appendErrorMessage(err) {
    const list = document.getElementById('chatList');
    const row = document.createElement('div');
    row.className = 'chat-msg-row agent';
    row.innerHTML = `
        <div class="msg-avatar" style="border-color: #ef4444;">⚠️</div>
        <div class="msg-bubble" style="border-left: 3px solid #ef4444; color: #fca5a5;">
            ${err}
        </div>
    `;
    list.appendChild(row);
}

function scrollChatToBottom() {
    const viewport = document.getElementById('chatViewport');
    if (viewport) viewport.scrollTop = viewport.scrollHeight;
}

function speakText(text) {
    if (!('speechSynthesis' in window)) {
        showToast('Text-to-speech not supported in this browser.');
        return;
    }
    window.speechSynthesis.cancel();
    const cleanText = text.replace(/[*#`_\[\]()]/g, ' ').substring(0, 450);
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.lang = state.lang === 'ka' ? 'ka-GE' : 'en-US';
    utterance.rate = 1.0;

    const waveEl = document.getElementById('agentVoiceWave');
    if (waveEl) waveEl.classList.remove('hidden');

    utterance.onend = () => { if (waveEl) waveEl.classList.add('hidden'); };
    utterance.onerror = () => { if (waveEl) waveEl.classList.add('hidden'); };

    window.speechSynthesis.speak(utterance);
}

async function resetChat() {
    try {
        await fetch('/api/reset', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sessionId: state.sessionId, agent: 'all' })
        });
        const list = document.getElementById('chatList');
        if (list) {
            list.innerHTML = `
                <div class="system-welcome-card animated-fade-in" id="welcomeCard">
                    <div class="welcome-header">
                        <div class="welcome-badge">🦉 რა? სად? როდის? — ინტელექტ-კლუბი</div>
                        <h3>მოგესალმებათ მოაზროვნეთა გუნდი!</h3>
                        <p>კაპიტანი ალექსი და ჩვენი 5 სპეციალიზებული ექსპერტი მზად არიან ნებისმიერ ინტელექტუალურ გამოწვევასა და შეკითხვაზე საპასუხოდ.</p>
                    </div>
                    <div class="quick-prompts-container">
                        <span class="quick-title">${state.lang === 'ka' ? i18n.ka.sample_prompts_title : i18n.en.sample_prompts_title}</span>
                        <div class="quick-pills-row" id="quickPillsRow"></div>
                    </div>
                </div>
            `;
            renderQuickPills();
        }
        showToast(state.lang === 'ka' ? i18n.ka.toast_reset : i18n.en.toast_reset);
    } catch (e) {
        console.error(e);
    }
}

// ==========================================
// 10. 1 წუთი ფიქრისთვის (ROUNDTABLE)
// ==========================================
async function submitSyndicate() {
    const input = document.getElementById('syndicateInput');
    const stream = document.getElementById('syndicateStream');
    const submitBtn = document.getElementById('syndicateSubmitBtn');
    if (!input || !stream) return;

    const topic = input.value.trim();
    if (!topic) return;

    submitBtn.disabled = true;
    submitBtn.style.opacity = '0.6';

    stream.innerHTML = `
        <div class="empty-syndicate-state glass-panel-glow">
            <div class="empty-hex pulse-glow-hex">🦉</div>
            <h3>${state.lang === 'ka' ? 'გავიდა 1 წუთი ფიქრისთვის...' : '1-minute countdown active...'}</h3>
            <p>${state.lang === 'ka' ? 'კაპიტანი, თეა, სანდრო, ლუკა, ნინო და დავითი მსჯელობენ.' : 'Captain, Tea, Sandro, Luka, Nino, and David are deliberating.'}</p>
        </div>
    `;

    playGongSound();

    try {
        const res = await fetch('/api/syndicate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: topic,
                sessionId: state.sessionId
            })
        });

        const data = await res.json();
        submitBtn.disabled = false;
        submitBtn.style.opacity = '1';

        if (data.success && data.data && data.data.contributions) {
            renderSyndicateStream(data.data.contributions);
            playChimeSound();
        } else {
            stream.innerHTML = `<div class="empty-syndicate-state"><p style="color:#ef4444;">${data.error || 'შეცდომა განხილვისას'}</p></div>`;
        }
    } catch (e) {
        submitBtn.disabled = false;
        submitBtn.style.opacity = '1';
        stream.innerHTML = `<div class="empty-syndicate-state"><p style="color:#ef4444;">ქსელის შეცდომა</p></div>`;
    }
}

function renderSyndicateStream(contributions) {
    const stream = document.getElementById('syndicateStream');
    if (!stream) return;
    stream.innerHTML = '';

    const isKa = state.lang === 'ka';

    contributions.forEach((step, idx) => {
        const card = document.createElement('div');
        const agent = state.agentsMeta[step.agent] || {
            name: step.agent,
            avatar: '👤',
            color: '#f59e0b'
        };

        const phaseClass = step.phase === 'framing' ? 'phase-framing' : (step.phase === 'synthesis' ? 'phase-synthesis' : 'phase-analysis');
        const phaseName = step.phase === 'framing' ? (isKa ? 'გახსნა' : 'Framing') : (step.phase === 'synthesis' ? (isKa ? 'საბოლოო პასუხი' : 'Final Answer') : (isKa ? 'ვერსია' : 'Clue'));

        card.className = `syndicate-step-card tilt-card ${step.agent}-step ${step.phase === 'synthesis' ? 'synthesis-step' : ''}`;
        card.style.animationDelay = `${idx * 0.12}s`;

        card.innerHTML = `
            <div class="syndicate-card-header">
                <div class="syndicate-agent-meta">
                    <div class="syndicate-step-avatar float-anim" style="border-color:${agent.color};">
                        ${agent.avatar}
                    </div>
                    <div>
                        <h4 class="syndicate-step-title" style="color: ${agent.color};">
                            ${isKa ? (step.title || agent.name) : (step.title_en || agent.name)}
                        </h4>
                        <span style="font-size: 0.72rem; color: var(--text-muted);">${agent.name}</span>
                    </div>
                </div>
                <span class="syndicate-step-phase ${phaseClass}">${phaseName}</span>
            </div>
            <div class="syndicate-card-content">
                ${formatMarkdown(step.content)}
            </div>
        `;
        stream.appendChild(card);
    });

    init3DTiltCards();
}

// ==========================================
// 11. QUIZ ARENA (ბროლის ბუ)
// ==========================================
async function loadNewQuizQuestion() {
    const qText = document.getElementById('quizQuestionText');
    const grid = document.getElementById('quizOptionsGrid');
    const explBox = document.getElementById('quizExplanationBox');

    if (!qText || !grid) return;

    state.quiz.answered = false;
    explBox.classList.add('hidden');
    qText.textContent = state.lang === 'ka' ? 'გენერირდება რაუნდის შეკითხვა...' : 'Generating quiz challenge...';
    grid.innerHTML = '';

    try {
        const res = await fetch('/api/quiz', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                subject: state.quiz.subject,
                lang: state.lang
            })
        });

        const data = await res.json();
        if (data.success && data.quiz) {
            state.quiz.current = data.quiz;
            renderQuizCard(data.quiz);
        } else {
            qText.textContent = 'ვერ მოხერხდა შეკითხვის ჩატვირთვა. სცადეთ თავიდან.';
        }
    } catch (e) {
        qText.textContent = 'ქსელის შეცდომა შეკითხვის ჩატვირთვისას.';
    }
}

function renderQuizCard(quiz) {
    const isKa = state.lang === 'ka';
    const qText = document.getElementById('quizQuestionText');
    const grid = document.getElementById('quizOptionsGrid');
    const avatar = document.getElementById('quizAgentAvatar');
    const name = document.getElementById('quizAgentName');
    const cat = document.getElementById('quizCategoryTag');

    const agentMeta = state.agentsMeta[quiz.agent] || { avatar: '🦉', name: 'რა? სად? როდის?' };
    if (avatar) avatar.textContent = agentMeta.avatar;
    if (name) name.textContent = agentMeta.name;
    if (cat) cat.textContent = `სფერო: ${quiz.subject.toUpperCase()}`;

    qText.textContent = isKa ? quiz.question_ka : quiz.question_en;
    grid.innerHTML = '';

    const options = isKa ? quiz.options_ka : quiz.options_en;
    const letters = ['A', 'B', 'C', 'D'];

    options.forEach((optText, idx) => {
        const btn = document.createElement('button');
        btn.className = 'quiz-opt-btn hover-lift';
        btn.innerHTML = `
            <span class="opt-letter">${letters[idx]}</span>
            <span>${optText}</span>
        `;
        btn.addEventListener('click', () => handleQuizAnswer(idx, btn));
        grid.appendChild(btn);
    });
}

function handleQuizAnswer(selectedIndex, selectedBtn) {
    if (state.quiz.answered || !state.quiz.current) return;
    state.quiz.answered = true;

    const quiz = state.quiz.current;
    const isCorrect = selectedIndex === quiz.correct_index;
    const isKa = state.lang === 'ka';

    const allButtons = document.querySelectorAll('.quiz-opt-btn');
    allButtons.forEach((btn, idx) => {
        btn.disabled = true;
        if (idx === quiz.correct_index) {
            btn.classList.add('correct');
        } else if (idx === selectedIndex && !isCorrect) {
            btn.classList.add('wrong');
        }
    });

    if (isCorrect) {
        state.quiz.score += 100;
        state.quiz.streak += 1;
        playCorrectSound();
        launchConfetti();
    } else {
        state.quiz.streak = 0;
        playWrongSound();
    }

    localStorage.setItem('ra_quiz_score', state.quiz.score);
    localStorage.setItem('ra_quiz_streak', state.quiz.streak);
    updateQuizStatsDisplay();

    const explBox = document.getElementById('quizExplanationBox');
    const statusEl = document.getElementById('explanationStatus');
    const textEl = document.getElementById('explanationText');

    if (explBox && statusEl && textEl) {
        explBox.classList.remove('hidden');
        if (isCorrect) {
            statusEl.className = 'explanation-status status-correct';
            statusEl.textContent = isKa ? i18n.ka.correct_title : i18n.en.correct_title;
        } else {
            statusEl.className = 'explanation-status status-wrong';
            statusEl.textContent = isKa ? i18n.ka.wrong_title : i18n.en.wrong_title;
        }
        textEl.textContent = isKa ? quiz.explanation_ka : quiz.explanation_en;
    }
}

function updateQuizStatsDisplay() {
    const scoreVal = document.getElementById('quizScoreVal');
    const streakVal = document.getElementById('quizStreakVal');
    const lvlVal = document.getElementById('quizLevelVal');

    if (scoreVal) scoreVal.textContent = state.quiz.score;
    if (streakVal) streakVal.textContent = state.quiz.streak;

    if (lvlVal) {
        const s = state.quiz.score;
        let lvl = 'მოაზროვნე (Lvl 1)';
        if (s >= 1000) lvl = 'ბროლის ბუს მფლობელი 🦉';
        else if (s >= 600) lvl = 'მაგისტრი 🔮';
        else if (s >= 300) lvl = 'გუნდის წამყვანი 📜';
        else if (s >= 100) lvl = 'გამჭრიახი ⚡';
        lvlVal.textContent = lvl;
    }
}

// ==========================================
// 12. INITIALIZATION & EVENT WIRING
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    initNeuralCanvas();
    init3DTiltCards();
    fetchAgentsMetadata();
    updateLanguageUI();
    updateQuizStatsDisplay();

    // Tab Navigation
    document.querySelectorAll('.nav-tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const tab = btn.getAttribute('data-tab');
            state.activeTab = tab;

            document.querySelectorAll('.nav-tab-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            document.querySelectorAll('.tab-view').forEach(view => view.classList.remove('active'));
            const targetView = document.getElementById('view' + tab.charAt(0).toUpperCase() + tab.slice(1));
            if (targetView) targetView.classList.add('active');

            if (tab === 'quiz' && !state.quiz.current) {
                loadNewQuizQuestion();
            }

            setTimeout(init3DTiltCards, 50);
        });
    });

    // Agent Selector Chips
    document.querySelectorAll('.agent-card-chip').forEach(chip => {
        chip.addEventListener('click', () => {
            const agentId = chip.getAttribute('data-agent-id');
            state.activeAgent = agentId;

            document.querySelectorAll('.agent-card-chip').forEach(c => c.classList.remove('active'));
            chip.classList.add('active');

            updateActiveAgentBanner();
            renderQuickPills();
        });
    });

    // Chat Form Submit
    const chatForm = document.getElementById('chatForm');
    if (chatForm) {
        chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            submitChatMessage();
        });
    }

    // Chat Textarea Enter Key handling
    const chatInput = document.getElementById('chatInput');
    if (chatInput) {
        chatInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                submitChatMessage();
            }
        });
    }

    // Reset Chat Button
    const btnReset = document.getElementById('btnResetChat');
    if (btnReset) {
        btnReset.addEventListener('click', resetChat);
    }

    // Syndicate Form & Presets
    const syndicateForm = document.getElementById('syndicateForm');
    if (syndicateForm) {
        syndicateForm.addEventListener('submit', (e) => {
            e.preventDefault();
            submitSyndicate();
        });
    }

    document.querySelectorAll('.preset-btn').forEach(pBtn => {
        pBtn.addEventListener('click', () => {
            const topic = pBtn.getAttribute('data-topic');
            const synInput = document.getElementById('syndicateInput');
            if (synInput) {
                synInput.value = topic;
                synInput.focus();
                submitSyndicate();
            }
        });
    });

    // Quiz Filter Buttons
    document.querySelectorAll('.subj-filter-btn').forEach(fBtn => {
        fBtn.addEventListener('click', () => {
            document.querySelectorAll('.subj-filter-btn').forEach(b => b.classList.remove('active'));
            fBtn.classList.add('active');
            state.quiz.subject = fBtn.getAttribute('data-subj');
            loadNewQuizQuestion();
        });
    });

    // Quiz Next Question Button
    const btnNextQuiz = document.getElementById('btnNextQuiz');
    if (btnNextQuiz) {
        btnNextQuiz.addEventListener('click', loadNewQuizQuestion);
    }

    // Language Toggle
    const langBtn = document.getElementById('langSwitchBtn');
    if (langBtn) {
        langBtn.addEventListener('click', toggleLanguage);
    }

    // Audio Sound Toggle
    const audioBtn = document.getElementById('audioToggleBtn');
    const audioIcon = document.getElementById('audioIcon');
    if (audioBtn) {
        audioBtn.addEventListener('click', () => {
            state.soundEnabled = !state.soundEnabled;
            localStorage.setItem('ra_sound', state.soundEnabled);
            if (audioIcon) {
                audioIcon.textContent = state.soundEnabled ? '🔊' : '🔇';
            }
            showToast(state.soundEnabled ? "ხმა ჩართულია" : "ხმა გათიშულია");
            if (state.soundEnabled) playTone(440, 'sine', 0.15);
        });
        if (audioIcon) {
            audioIcon.textContent = state.soundEnabled ? '🔊' : '🔇';
        }
    }

    // Dossier "Chat With" Buttons
    document.querySelectorAll('.btn-chat-with').forEach(btn => {
        btn.addEventListener('click', () => {
            const agent = btn.getAttribute('data-agent');
            state.activeAgent = agent;

            document.getElementById('tabBtnChat').click();

            document.querySelectorAll('.agent-card-chip').forEach(c => {
                if (c.getAttribute('data-agent-id') === agent) {
                    c.click();
                }
            });
        });
    });
});
