/**
 * Evaluación ISO/IEC 25010 — puntuación + persistencia local
 */
(function () {
  'use strict';

  const STORAGE_KEY = 'guia-iso-eval';
  const CHARS = ['adec', 'efic', 'compat', 'inter', 'fiab', 'seg', 'mant', 'flex', 'prot'];

  const CHAR_NAMES = {
    adec: 'Adecuación Funcional',
    efic: 'Eficiencia Desempeño',
    compat: 'Compatibilidad',
    inter: 'Capacidad Interacción',
    fiab: 'Fiabilidad',
    seg: 'Seguridad',
    mant: 'Mantenibilidad',
    flex: 'Flexibilidad',
    prot: 'Protección',
  };

  function getCharScore(char) {
    const rows = document.querySelectorAll('.q-row[data-char="' + char + '"]');
    let total = 0;
    let answered = 0;
    rows.forEach((_, i) => {
      const sel = document.querySelector('input[name="' + char + '_' + (i + 1) + '"]:checked');
      if (sel) {
        total += parseInt(sel.value, 10);
        answered++;
      }
    });
    return { total, answered, max: rows.length * 4, questions: rows.length };
  }

  window.getCharScore = getCharScore;

  function saveAnswers() {
    const data = {};
    document.querySelectorAll('.q-opt input[type="radio"]:checked').forEach((inp) => {
      data[inp.name] = inp.value;
    });
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    } catch { /* ignore */ }
  }

  function restoreAnswers() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return;
      const data = JSON.parse(raw);
      Object.keys(data).forEach((name) => {
        const inp = document.querySelector(
          'input[name="' + name + '"][value="' + data[name] + '"]'
        );
        if (inp) inp.checked = true;
      });
    } catch { /* ignore */ }
  }

  function openAllCharacteristics() {
    document.querySelectorAll('.iso-char-body').forEach((body) => {
      body.classList.add('open');
      body.style.display = 'block';
    });
    document.querySelectorAll('.iso-char-head').forEach((head) => {
      head.setAttribute('aria-expanded', 'true');
    });
  }

  window.updateDashboard = function updateDashboard() {
    let totalAnswered = 0;
    let totalScore = 0;

    CHARS.forEach((c) => {
      const s = getCharScore(c);
      totalAnswered += s.answered;
      totalScore += s.total;
      const pct = s.answered > 0 ? Math.round((s.total / (s.answered * 4)) * 100) : 0;
      const el = document.querySelector('.iso-char-pct[data-char="' + c + '"]');
      if (el) {
        el.textContent =
          s.answered === s.questions ? pct + '%' : s.answered + '/' + s.questions;
        const fill = el.closest('.iso-char-score');
        const bar = fill && fill.querySelector('.iso-char-fill');
        if (bar) bar.style.width = pct + '%';
      }
    });

    const overallPct =
      totalAnswered > 0 ? Math.round((totalScore / (totalAnswered * 4)) * 100) : 0;
    const totalResp = document.getElementById('totalResp');
    const respFill = document.getElementById('respFill');
    const totalScoreEl = document.getElementById('totalScore');
    const totalPctEl = document.getElementById('totalPct');
    const totalFill = document.getElementById('totalFill');
    const pctFill = document.getElementById('pctFill');

    if (totalResp) totalResp.textContent = String(totalAnswered);
    if (respFill) respFill.style.width = (totalAnswered / 27) * 100 + '%';

    if (totalAnswered > 0) {
      if (totalScoreEl) totalScoreEl.textContent = totalScore + '/' + totalAnswered * 4;
      if (totalPctEl) totalPctEl.textContent = overallPct + '%';
      if (totalFill) totalFill.style.width = overallPct + '%';
      if (pctFill) pctFill.style.width = overallPct + '%';
    }

    saveAnswers();
  };

  window.calcScore = function calcScore() {
    const unanswered = [];
    let totalScore = 0;
    let totalMax = 0;

    CHARS.forEach((c) => {
      const rows = document.querySelectorAll('.q-row[data-char="' + c + '"]');
      rows.forEach((_, i) => {
        const sel = document.querySelector('input[name="' + c + '_' + (i + 1) + '"]:checked');
        if (!sel) unanswered.push(CHAR_NAMES[c] + ' — Pregunta ' + (i + 1));
        else {
          totalScore += parseInt(sel.value, 10);
          totalMax += 4;
        }
      });
    });

    if (unanswered.length > 0) {
      const preview = unanswered.slice(0, 5).join('\n• ');
      const more =
        unanswered.length > 5 ? '\n• (y ' + (unanswered.length - 5) + ' más...)' : '';
      alert(
        'Por favor responde todas las preguntas antes de calcular.\n\nPendientes:\n• ' +
          preview +
          more
      );
      return;
    }

    const pct = Math.round((totalScore / totalMax) * 100);
    let label = '';
    let color = '';

    if (pct >= 85) {
      label = 'Excelente cumplimiento';
      color = 'var(--status-success)';
    } else if (pct >= 70) {
      label = 'Buen cumplimiento';
      color = '#5a8f29';
    } else if (pct >= 55) {
      label = 'Cumplimiento parcial';
      color = 'var(--status-warning)';
    } else {
      label = 'Requiere mejoras significativas';
      color = 'var(--status-error)';
    }

    const resultBig = document.getElementById('resultBig');
    const resultLabel = document.getElementById('resultLabel');
    const resultGrid = document.getElementById('resultGrid');
    const resultRec = document.getElementById('resultRec');
    const evalResult = document.getElementById('evalResult');

    if (resultBig) {
      resultBig.textContent = pct + '%';
      resultBig.style.color = color;
    }
    if (resultLabel) {
      resultLabel.textContent = label + ' · ' + totalScore + '/' + totalMax + ' puntos';
    }
    if (resultGrid) {
      resultGrid.innerHTML = CHARS.map((c) => {
        const s = getCharScore(c);
        const cp = Math.round((s.total / s.max) * 100);
        return (
          '<div class="result-item"><div class="result-item-name">' +
          CHAR_NAMES[c] +
          '</div><div class="result-item-val">' +
          cp +
          '%</div></div>'
        );
      }).join('');
    }

    const weakest = CHARS.filter((c) => {
      const s = getCharScore(c);
      return s.total / s.max < 0.6;
    }).map((c) => CHAR_NAMES[c]);

    if (resultRec) {
      resultRec.innerHTML =
        weakest.length > 0
          ? '<strong>Áreas prioritarias de mejora:</strong> ' +
            weakest.join(', ') +
            '. Revisa los módulos del handbook y registra evidencias en <a href="evidencias.html">Registro de evidencias</a>.'
          : '<strong>Excelente resultado.</strong> Tu proyecto muestra un alto nivel de cumplimiento ISO/IEC 25010.';
    }

    if (evalResult) {
      evalResult.classList.add('show');
      evalResult.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  window.resetEval = function resetEval() {
    if (!confirm('¿Reiniciar todas las respuestas de la evaluación?')) return;

    document.querySelectorAll('.q-opt input').forEach((i) => {
      i.checked = false;
    });
    try {
      localStorage.removeItem(STORAGE_KEY);
    } catch { /* ignore */ }

    const evalResult = document.getElementById('evalResult');
    if (evalResult) evalResult.classList.remove('show');

    CHARS.forEach((c) => {
      const el = document.querySelector('.iso-char-pct[data-char="' + c + '"]');
      if (el) {
        el.textContent = '—';
        const fill = el.closest('.iso-char-score');
        const bar = fill && fill.querySelector('.iso-char-fill');
        if (bar) bar.style.width = '0%';
      }
    });

    ['totalScore', 'totalPct'].forEach((id) => {
      const el = document.getElementById(id);
      if (el) el.textContent = '—';
    });
    const totalResp = document.getElementById('totalResp');
    if (totalResp) totalResp.textContent = '0';
    ['totalFill', 'pctFill', 'respFill'].forEach((id) => {
      const el = document.getElementById(id);
      if (el) el.style.width = '0%';
    });

    updateDashboard();
  };

  document.addEventListener('DOMContentLoaded', () => {
    if (!document.querySelector('.q-row')) return;

    openAllCharacteristics();
    restoreAnswers();

    document.querySelectorAll('.q-opt input').forEach((inp) => {
      inp.addEventListener('change', updateDashboard);
    });

    updateDashboard();
  });
})();
