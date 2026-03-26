"""
SoloOS V10 — Streamlit Dashboard

Multi-page founder intelligence dashboard. Reads directly from SQLite (context_db)
and DuckDB (analytics_db) — no MCP server required to be running.

Run:
    cd mcp/soloos-core
    streamlit run dashboard/app.py

Pages:
    Morning Brief     — kill signals, MRR snapshot, recent decisions
    Decision History  — searchable table, log new decisions
    KPI Dashboard     — MRR trend, churn gauge, runway (DuckDB-backed)
    Experiments       — running/completed experiments, log new hypothesis

Env vars: none required. Graceful empty state when no data is connected.
"""

from __future__ import annotations

import sys
import os
from pathlib import Path

# ── Make soloos_core importable from the src/ layout ──────────────────────────
_REPO_ROOT = Path(__file__).resolve().parent.parent
_SRC_DIR = _REPO_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

# ── Stdlib / third-party ───────────────────────────────────────────────────────
import datetime
import uuid
import traceback

import streamlit as st

# ── Lazy imports for soloos_core modules (fail-open) ──────────────────────────

def _load_analytics_db():
    """Return AnalyticsDB singleton or None on import failure."""
    try:
        from soloos_core.data.analytics_db import get_analytics_db
        return get_analytics_db()
    except Exception:
        return None


def _load_context_db():
    """Return ContextDB singleton or None on import failure."""
    try:
        from soloos_core.data.context_db import get_context_db
        return get_context_db()
    except Exception:
        return None


def _load_log_manager():
    """Return the log_manager module or None on import failure."""
    try:
        import soloos_core.log_manager as lm
        return lm
    except Exception:
        return None


# ── Plotly import (optional — soft dep) ───────────────────────────────────────
try:
    import plotly.graph_objects as go
    import plotly.express as px
    _PLOTLY_OK = True
except ImportError:
    _PLOTLY_OK = False


# ══════════════════════════════════════════════════════════════════════════════
# Page config (must be first Streamlit call)
# ══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title='SoloOS Dashboard',
    page_icon=':bar_chart:',
    layout='wide',
    initial_sidebar_state='expanded',
)

# ── Light CSS tweaks ───────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .metric-card {
        background: #1e1e2e;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 8px;
    }
    .kill-signal-overdue {
        background: #3d1414;
        border-left: 4px solid #ff4444;
        padding: 12px 16px;
        border-radius: 4px;
        margin-bottom: 8px;
    }
    .kill-signal-urgent {
        background: #3d2d10;
        border-left: 4px solid #ff8c00;
        padding: 12px 16px;
        border-radius: 4px;
        margin-bottom: 8px;
    }
    .status-badge-running  { color: #4caf50; font-weight: 600; }
    .status-badge-completed { color: #2196f3; font-weight: 600; }
    .status-badge-abandoned { color: #9e9e9e; font-weight: 600; }
    .empty-state {
        text-align: center;
        color: #666;
        padding: 40px 20px;
        border: 1px dashed #333;
        border-radius: 8px;
        margin: 20px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ══════════════════════════════════════════════════════════════════════════════
# Sidebar — navigation + data source status
# ══════════════════════════════════════════════════════════════════════════════

def _connector_dot(configured: bool) -> str:
    return ':green_circle:' if configured else ':white_circle:'


def render_sidebar() -> str:
    """Render sidebar navigation and data source status. Returns selected page name."""
    with st.sidebar:
        st.title('SoloOS V10')
        st.caption('Founder Intelligence Dashboard')
        st.divider()

        page = st.radio(
            'Navigate',
            ['Morning Brief', 'Decision History', 'KPI Dashboard', 'Experiments'],
            label_visibility='collapsed',
        )

        st.divider()
        st.subheader('DATA SOURCES')

        # Analytics DB (DuckDB)
        adb = _load_analytics_db()
        adb_ok = adb is not None and adb._initialized
        st.write(f'{_connector_dot(adb_ok)} DuckDB analytics')

        # Context DB (SQLite)
        cdb = _load_context_db()
        cdb_ok = cdb is not None and cdb.is_available()
        st.write(f'{_connector_dot(cdb_ok)} SQLite context')

        # Stripe
        stripe_ok = bool(os.environ.get('STRIPE_API_KEY'))
        st.write(f'{_connector_dot(stripe_ok)} Stripe')

        # Mercury
        mercury_ok = bool(os.environ.get('MERCURY_API_KEY'))
        st.write(f'{_connector_dot(mercury_ok)} Mercury')

        # PostHog
        posthog_ok = bool(os.environ.get('POSTHOG_API_KEY'))
        st.write(f'{_connector_dot(posthog_ok)} PostHog')

        # REST API (soloos-api)
        api_base = os.environ.get('SOLOOS_API_URL', 'http://localhost:8765')
        try:
            import urllib.request
            urllib.request.urlopen(f'{api_base}/', timeout=1)
            api_ok = True
        except Exception:
            api_ok = False
        st.write(f'{_connector_dot(api_ok)} SoloOS REST API')

        st.divider()
        st.caption(f'Today: {datetime.date.today().isoformat()}')

    return page


# ══════════════════════════════════════════════════════════════════════════════
# Page 1 — Morning Brief
# ══════════════════════════════════════════════════════════════════════════════

def _render_kill_signal_card(alert: dict, source: str = 'sqlite') -> None:
    """Render a single kill signal alert card."""
    urgency = alert.get('urgency', 'OK')
    entry_id = alert.get('entry_id', alert.get('id', '?'))
    summary = alert.get('summary', alert.get('decision', ''))
    ks = alert.get('kill_signal', '')
    due = alert.get('due_date', alert.get('kill_signal_date', ''))
    days = alert.get('days_remaining')

    if urgency == 'OVERDUE':
        css = 'kill-signal-overdue'
        label = 'OVERDUE'
    elif urgency == 'URGENT':
        css = 'kill-signal-urgent'
        label = 'URGENT'
    else:
        css = 'kill-signal-urgent'
        label = 'WARNING'

    days_str = f'{abs(days)} days overdue' if (days is not None and days < 0) else (
        f'{days} days left' if days is not None else 'check date'
    )

    st.markdown(
        f"""
        <div class="{css}">
            <strong>{label}: [{entry_id}]</strong> — {days_str}<br>
            <em>{summary[:120]}</em><br>
            <small>Kill signal: {ks[:100]} | Due: {due}</small>
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_morning_brief() -> None:
    st.header('Morning Brief')
    st.caption('Kill signals, MRR snapshot, recent decisions.')

    # ── Kill Signals ──────────────────────────────────────────────────────────
    st.subheader('Kill Signals')

    kill_signals: list[dict] = []

    # Try context_db first (SQLite)
    cdb = _load_context_db()
    if cdb and cdb.is_available():
        pending = cdb.get_pending_kill_signals()
        now = datetime.datetime.now()
        for row in pending:
            ks_date_str = row.get('kill_signal_date') or ''
            try:
                ks_dt = datetime.datetime.strptime(ks_date_str, '%Y-%m-%d')
                days_left = (ks_dt - now).days
                if days_left < 0:
                    urgency = 'OVERDUE'
                elif days_left <= 7:
                    urgency = 'URGENT'
                elif days_left <= 14:
                    urgency = 'WARNING'
                else:
                    urgency = 'OK'
            except Exception:
                days_left = None
                urgency = 'OK'
            kill_signals.append({
                'entry_id': row.get('id', '?'),
                'summary': row.get('decision', ''),
                'kill_signal': row.get('kill_signal', ''),
                'due_date': ks_date_str,
                'days_remaining': days_left,
                'urgency': urgency,
            })

    # Fall back to log_manager markdown parser
    if not kill_signals:
        lm = _load_log_manager()
        if lm:
            try:
                entries = lm.load_log()
                alerts = lm.check_kill_signals(entries)
                for a in alerts:
                    kill_signals.append({
                        'entry_id': a.entry_id,
                        'summary': a.summary,
                        'kill_signal': a.kill_signal,
                        'due_date': a.due_date,
                        'days_remaining': a.days_remaining,
                        'urgency': a.urgency,
                    })
            except Exception:
                pass

    overdue = [k for k in kill_signals if k['urgency'] == 'OVERDUE']
    urgent = [k for k in kill_signals if k['urgency'] == 'URGENT']
    warning = [k for k in kill_signals if k['urgency'] == 'WARNING']

    if not kill_signals:
        st.success('No pending kill signals. All clear.')
    else:
        if overdue:
            st.error(f'{len(overdue)} OVERDUE kill signal(s) — action required now.')
            for k in overdue:
                _render_kill_signal_card(k)
        if urgent:
            st.warning(f'{len(urgent)} URGENT kill signal(s) — due within 7 days.')
            for k in urgent:
                _render_kill_signal_card(k)
        if warning:
            with st.expander(f'{len(warning)} warning(s) — due within 14 days'):
                for k in warning:
                    _render_kill_signal_card(k)

    st.divider()

    # ── MRR + Runway snapshot ─────────────────────────────────────────────────
    col1, col2, col3 = st.columns(3)

    adb = _load_analytics_db()
    mrr = 0.0
    has_revenue_data = False
    if adb and adb._initialized and adb.has_data():
        has_revenue_data = True
        mrr = adb.get_current_mrr()
        churn = adb.get_churn_rate()
    else:
        churn = 0.0

    with col1:
        if has_revenue_data:
            st.metric('Current MRR', f'${mrr:,.0f}')
        else:
            st.metric('Current MRR', 'No data')
            st.caption('Connect Stripe to see live MRR')

    with col2:
        if has_revenue_data and mrr > 0:
            est_arr = mrr * 12
            st.metric('Est. ARR', f'${est_arr:,.0f}')
        else:
            st.metric('Est. ARR', '—')

    with col3:
        if has_revenue_data and churn > 0:
            st.metric('Churn Rate', f'{churn:.1%}')
        else:
            st.metric('Churn Rate', '—')

    st.divider()

    # ── Recent decisions ──────────────────────────────────────────────────────
    st.subheader('3 Most Recent Decisions')

    recent: list[dict] = []
    if cdb and cdb.is_available():
        recent = cdb.list_decisions(limit=3)
    elif _load_log_manager():
        lm = _load_log_manager()
        try:
            entries = lm.load_log()[:3]
            for e in entries:
                recent.append({
                    'id': e.id,
                    'date': e.date,
                    'decision': e.summary,
                    'kill_signal': e.kill_signal,
                    'outcome': e.outcome,
                })
        except Exception:
            pass

    if not recent:
        st.markdown(
            '<div class="empty-state">No decisions logged yet.<br>'
            'Use the Decision History page to log your first decision.</div>',
            unsafe_allow_html=True,
        )
    else:
        for row in recent:
            with st.container():
                id_val = row.get('id', '?')
                date_val = row.get('date', '')
                decision_val = row.get('decision', '')
                ks_val = row.get('kill_signal', '') or ''
                outcome_val = row.get('outcome', '') or ''
                st.markdown(
                    f'**[{id_val}]** {date_val}  \n'
                    f'{decision_val[:200]}  \n'
                    + (f'*Kill signal: {ks_val[:80]}*' if ks_val else '')
                    + ('  :white_check_mark: Outcome logged' if outcome_val else ''),
                )
                st.divider()

    # ── Run Full Brief button ─────────────────────────────────────────────────
    st.subheader('Full Brief')
    api_base = os.environ.get('SOLOOS_API_URL', 'http://localhost:8765')
    if st.button('Run Full Morning Brief (via REST API)'):
        try:
            import urllib.request
            import json as _json
            req = urllib.request.Request(
                f'{api_base}/tools/run_morning_brief',
                data=b'{}',
                headers={'Content-Type': 'application/json'},
                method='POST',
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                body = _json.loads(resp.read())
            st.success('Brief complete.')
            st.code(str(body)[:2000], language='json')
        except Exception as exc:
            st.info(
                f'SoloOS REST API not reachable at {api_base}. '
                f'Start with: `soloos-api --port 8765`\n\n'
                f'Error: {exc}'
            )


# ══════════════════════════════════════════════════════════════════════════════
# Page 2 — Decision History
# ══════════════════════════════════════════════════════════════════════════════

def page_decision_history() -> None:
    st.header('Decision History')

    cdb = _load_context_db()

    # ── Search ────────────────────────────────────────────────────────────────
    search_term = st.text_input('Search decisions', placeholder='Type to filter...')

    # ── Load decisions ────────────────────────────────────────────────────────
    decisions: list[dict] = []
    if cdb and cdb.is_available():
        decisions = cdb.list_decisions(limit=500)
    else:
        lm = _load_log_manager()
        if lm:
            try:
                entries = lm.load_log()
                for e in entries:
                    decisions.append({
                        'id': e.id,
                        'date': e.date,
                        'decision': e.summary,
                        'situation': e.context,
                        'kill_signal': e.kill_signal,
                        'kill_signal_date': e.kill_signal_due,
                        'outcome': e.outcome if e.outcome != 'PENDING OUTCOME' else None,
                        'tags': e.type,
                    })
            except Exception:
                pass

    # Filter by search
    if search_term:
        term = search_term.lower()
        decisions = [
            d for d in decisions
            if term in (d.get('decision') or '').lower()
            or term in (d.get('situation') or '').lower()
            or term in (d.get('kill_signal') or '').lower()
            or term in (d.get('id') or '').lower()
        ]

    st.caption(f'{len(decisions)} decision(s) found')

    if not decisions:
        st.markdown(
            '<div class="empty-state">No decisions found.<br>'
            'Log your first decision below.</div>',
            unsafe_allow_html=True,
        )
    else:
        # ── Table ─────────────────────────────────────────────────────────────
        import pandas as pd

        table_rows = []
        for d in decisions:
            outcome_raw = d.get('outcome') or ''
            if outcome_raw and outcome_raw != 'PENDING OUTCOME':
                status = 'Resolved'
            elif d.get('kill_signal'):
                status = 'Pending'
            else:
                status = '—'

            table_rows.append({
                'ID': d.get('id', ''),
                'Date': d.get('date', ''),
                'Decision': (d.get('decision') or '')[:80] + ('...' if len(d.get('decision') or '') > 80 else ''),
                'Kill Signal': (d.get('kill_signal') or '')[:60] + ('...' if len(d.get('kill_signal') or '') > 60 else ''),
                'Status': status,
            })

        df = pd.DataFrame(table_rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # ── Row expander ──────────────────────────────────────────────────────
        st.subheader('Expand a decision')
        decision_ids = [d.get('id', '') for d in decisions if d.get('id')]
        if decision_ids:
            selected_id = st.selectbox('Select decision ID', decision_ids)
            selected = next((d for d in decisions if d.get('id') == selected_id), None)
            if selected:
                with st.expander(f'Full detail: {selected_id}', expanded=True):
                    st.markdown(f'**ID:** {selected.get("id")}')
                    st.markdown(f'**Date:** {selected.get("date")}')
                    st.markdown(f'**Decision:** {selected.get("decision")}')
                    st.markdown(f'**Situation:** {selected.get("situation") or "—"}')
                    st.markdown(f'**Kill Signal:** {selected.get("kill_signal") or "—"}')
                    st.markdown(f'**Kill Signal Date:** {selected.get("kill_signal_date") or "—"}')
                    outcome = selected.get('outcome') or ''
                    if outcome and outcome != 'PENDING OUTCOME':
                        st.markdown(f'**Outcome:** {outcome}')
                    else:
                        st.markdown('**Outcome:** Pending')
                    st.markdown(f'**Tags:** {selected.get("tags") or "—"}')

    st.divider()

    # ── Log New Decision form ─────────────────────────────────────────────────
    st.subheader('Log New Decision')

    with st.form('log_decision_form', clear_on_submit=True):
        col_a, col_b = st.columns([1, 2])
        with col_a:
            decision_type = st.selectbox('Type', ['Decision', 'Experiment', 'Pivot', 'Other'])
            decision_date = st.date_input('Date', value=datetime.date.today())
        with col_b:
            summary = st.text_input('Decision (one sentence)', max_chars=200)
            situation = st.text_area('Situation / Context', height=80)

        kill_signal = st.text_input('Kill signal', placeholder='If X does not happen by...')
        ks_date_col, _ = st.columns([1, 2])
        with ks_date_col:
            ks_date = st.date_input(
                'Kill signal due date',
                value=datetime.date.today() + datetime.timedelta(days=30),
            )
        tags = st.text_input('Tags (comma-separated)', placeholder='pricing, experiment, ICP')

        submitted = st.form_submit_button('Log Decision')

    if submitted:
        if not summary.strip():
            st.error('Decision summary is required.')
        else:
            # Generate ID
            new_id = 'FL-001'
            if cdb and cdb.is_available():
                existing = cdb.list_decisions(limit=1000)
                if existing:
                    nums = []
                    for d in existing:
                        id_str = d.get('id', '')
                        if id_str.startswith('FL-'):
                            try:
                                nums.append(int(id_str.split('-')[1]))
                            except Exception:
                                pass
                    if nums:
                        new_id = f'FL-{max(nums) + 1:03d}'

            ok = False
            if cdb and cdb.is_available():
                ok = cdb.upsert_decision(
                    id=new_id,
                    date=decision_date.isoformat(),
                    situation=situation.strip(),
                    decision=summary.strip(),
                    kill_signal=kill_signal.strip() or None,
                    kill_signal_date=ks_date.isoformat() if kill_signal.strip() else None,
                    tags=tags.strip() or decision_type,
                )
            else:
                # Fallback: use log_manager to write markdown
                lm = _load_log_manager()
                if lm:
                    try:
                        entries = lm.load_log()
                        new_id = lm.next_log_id(entries)
                        from soloos_core.log_manager import FounderLogEntry
                        entry = FounderLogEntry(
                            id=new_id,
                            date=decision_date.isoformat(),
                            type=decision_type,
                            summary=summary.strip(),
                            context=situation.strip(),
                            pattern_applied='',
                            hypothesis='',
                            kill_signal=kill_signal.strip(),
                            kill_signal_due=ks_date.isoformat(),
                            outcome='PENDING OUTCOME',
                            outcome_due=ks_date.isoformat(),
                            outcome_status='Pending',
                        )
                        lm.append_log_entry(entry)
                        ok = True
                    except Exception as exc:
                        st.error(f'Failed to write to markdown log: {exc}')
                else:
                    st.warning('No data store available. Install soloos-core package.')

            if ok:
                st.success(f'Decision logged as {new_id}.')
                st.rerun()
            elif not ok and not (cdb and cdb.is_available()):
                st.warning('Could not write to any data store. Check installation.')


# ══════════════════════════════════════════════════════════════════════════════
# Page 3 — KPI Dashboard
# ══════════════════════════════════════════════════════════════════════════════

def _empty_state_chart(label: str) -> None:
    st.markdown(
        f'<div class="empty-state">{label}</div>',
        unsafe_allow_html=True,
    )


def page_kpi_dashboard() -> None:
    st.header('KPI Dashboard')

    adb = _load_analytics_db()
    has_data = adb is not None and adb._initialized and adb.has_data()

    # ── Top metrics row ───────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if has_data:
            mrr = adb.get_current_mrr()
            st.metric('MRR', f'${mrr:,.0f}')
        else:
            st.metric('MRR', '—')

    with col2:
        if has_data:
            mrr = adb.get_current_mrr()
            st.metric('ARR (est.)', f'${mrr * 12:,.0f}')
        else:
            st.metric('ARR (est.)', '—')

    with col3:
        if has_data:
            churn = adb.get_churn_rate()
            st.metric('Churn Rate', f'{churn:.1%}')
        else:
            st.metric('Churn Rate', '—')

    with col4:
        # Runway placeholder — would connect to Mercury for cash balance
        mercury_key = os.environ.get('MERCURY_API_KEY')
        if mercury_key:
            st.metric('Runway', 'Connect Mercury')
        else:
            st.metric('Runway', '—')

    st.divider()

    if not _PLOTLY_OK:
        st.warning('plotly not installed. Run: pip install plotly')
        return

    # ── MRR Trend chart ───────────────────────────────────────────────────────
    st.subheader('MRR Trend (last 6 months)')

    if has_data:
        trend = adb.get_mrr_trend(months=6)
        if trend:
            import pandas as pd
            df_trend = pd.DataFrame(trend)
            df_trend['month'] = pd.to_datetime(df_trend['month'])
            df_trend = df_trend.sort_values('month')

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_trend['month'],
                y=df_trend['mrr_dollars'],
                mode='lines+markers',
                name='MRR',
                line=dict(color='#4caf50', width=2),
                marker=dict(size=6),
                fill='tozeroy',
                fillcolor='rgba(76, 175, 80, 0.1)',
            ))
            fig.update_layout(
                xaxis_title='Month',
                yaxis_title='MRR ($)',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=320,
                margin=dict(l=0, r=0, t=0, b=0),
                yaxis=dict(tickprefix='$', tickformat=',.0f'),
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            _empty_state_chart('MRR data loaded but no monthly events found yet.')
    else:
        _empty_state_chart('Connect Stripe to see live MRR trend data.')

    # ── Churn gauge ───────────────────────────────────────────────────────────
    st.subheader('Churn Rate Gauge')

    col_gauge, col_runway = st.columns(2)

    with col_gauge:
        if has_data:
            churn_rate = adb.get_churn_rate()
            fig_gauge = go.Figure(go.Indicator(
                mode='gauge+number',
                value=round(churn_rate * 100, 2),
                number={'suffix': '%', 'font': {'size': 28}},
                gauge={
                    'axis': {'range': [0, 20], 'ticksuffix': '%'},
                    'bar': {'color': '#ff4444' if churn_rate > 0.05 else '#4caf50'},
                    'steps': [
                        {'range': [0, 3], 'color': 'rgba(76,175,80,0.2)'},
                        {'range': [3, 7], 'color': 'rgba(255,165,0,0.2)'},
                        {'range': [7, 20], 'color': 'rgba(255,68,68,0.2)'},
                    ],
                    'threshold': {
                        'line': {'color': 'orange', 'width': 2},
                        'thickness': 0.75,
                        'value': 5,
                    },
                },
                title={'text': 'Monthly Churn', 'font': {'size': 14}},
            ))
            fig_gauge.update_layout(
                height=260,
                margin=dict(l=20, r=20, t=40, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
            )
            st.plotly_chart(fig_gauge, use_container_width=True)
        else:
            _empty_state_chart('Connect Stripe to see churn rate.')

    with col_runway:
        # Runway bar chart — placeholder unless Mercury connected
        st.subheader('Runway')
        if os.environ.get('MERCURY_API_KEY'):
            _empty_state_chart('Mercury connected — sync data to see runway chart.')
        else:
            _empty_state_chart(
                'Connect Mercury to see runway.<br>'
                'Set <code>MERCURY_API_KEY</code> env var.'
            )

    st.divider()

    # ── Sync state summary ────────────────────────────────────────────────────
    st.subheader('Data Sync Status')

    if adb and adb._initialized:
        sources = ['stripe', 'mercury', 'posthog']
        sync_rows = []
        for src in sources:
            state = adb.get_sync_state(src)
            sync_rows.append({
                'Source': src.capitalize(),
                'Last Synced': str(state.get('last_synced_at', 'Never')),
                'Status': state.get('status', 'not connected'),
                'Cursor': str(state.get('last_cursor', '—'))[:40],
            })

        import pandas as pd
        st.dataframe(pd.DataFrame(sync_rows), use_container_width=True, hide_index=True)
    else:
        _empty_state_chart('DuckDB not initialized — analytics data unavailable.')


# ══════════════════════════════════════════════════════════════════════════════
# Page 4 — Experiments
# ══════════════════════════════════════════════════════════════════════════════

def _status_badge(status: str) -> str:
    css_map = {
        'running': 'status-badge-running',
        'completed': 'status-badge-completed',
        'abandoned': 'status-badge-abandoned',
    }
    css = css_map.get(status.lower(), '')
    label = status.upper()
    return f'<span class="{css}">{label}</span>'


def page_experiments() -> None:
    st.header('Experiments')
    st.caption('Track hypotheses, A/B tests, and their outcomes.')

    cdb = _load_context_db()

    # ── Status filter ─────────────────────────────────────────────────────────
    status_filter = st.radio(
        'Filter by status',
        ['All', 'Running', 'Completed', 'Abandoned'],
        horizontal=True,
    )
    filter_val = None if status_filter == 'All' else status_filter.lower()

    # ── Load experiments ──────────────────────────────────────────────────────
    experiments: list[dict] = []
    if cdb and cdb.is_available():
        experiments = cdb.list_experiments(status=filter_val)

    st.caption(f'{len(experiments)} experiment(s)')

    if not experiments:
        st.markdown(
            '<div class="empty-state">No experiments found.<br>'
            'Log your first experiment hypothesis below.</div>',
            unsafe_allow_html=True,
        )
    else:
        for exp in experiments:
            exp_id = exp.get('id', '?')
            hypothesis = exp.get('hypothesis', '')
            status = exp.get('status', 'running')
            started = exp.get('started_at') or '—'
            completed = exp.get('completed_at') or '—'
            result = exp.get('result') or ''
            notes = exp.get('notes') or ''

            with st.expander(
                f'{exp_id} — {hypothesis[:80]}{"..." if len(hypothesis) > 80 else ""}',
                expanded=(status == 'running'),
            ):
                col_a, col_b = st.columns([2, 1])
                with col_a:
                    st.markdown(f'**Hypothesis:** {hypothesis}')
                    if result:
                        st.markdown(f'**Result:** {result}')
                    if notes:
                        st.markdown(f'**Notes:** {notes}')
                with col_b:
                    st.markdown(
                        f'**Status:** {_status_badge(status)}',
                        unsafe_allow_html=True,
                    )
                    st.markdown(f'**Started:** {started}')
                    if completed != '—':
                        st.markdown(f'**Completed:** {completed}')

                # Quick status update for running experiments
                if status == 'running' and cdb and cdb.is_available():
                    with st.form(f'update_exp_{exp_id}'):
                        new_status = st.selectbox(
                            'Update status',
                            ['running', 'completed', 'abandoned'],
                            key=f'status_{exp_id}',
                        )
                        new_result = st.text_input('Result / outcome', key=f'result_{exp_id}')
                        if st.form_submit_button('Update'):
                            completed_at = (
                                datetime.datetime.utcnow().isoformat()
                                if new_status != 'running'
                                else None
                            )
                            cdb.upsert_experiment(
                                id=exp_id,
                                hypothesis=hypothesis,
                                status=new_status,
                                started_at=exp.get('started_at'),
                                completed_at=completed_at,
                                result=new_result.strip() or result or None,
                                notes=notes or None,
                            )
                            st.success(f'Experiment {exp_id} updated.')
                            st.rerun()

    st.divider()

    # ── Log New Experiment form ───────────────────────────────────────────────
    st.subheader('Log New Experiment')

    with st.form('log_experiment_form', clear_on_submit=True):
        hypothesis = st.text_area(
            'Hypothesis',
            placeholder='If we [action], then [metric] will [change] because [reason].',
            height=100,
        )
        col_x, col_y = st.columns(2)
        with col_x:
            exp_start = st.date_input('Start date', value=datetime.date.today())
        with col_y:
            exp_notes = st.text_input('Notes / context', placeholder='Optional')

        submitted_exp = st.form_submit_button('Log Experiment')

    if submitted_exp:
        if not hypothesis.strip():
            st.error('Hypothesis is required.')
        else:
            exp_id = f'EXP-{uuid.uuid4().hex[:6].upper()}'
            if cdb and cdb.is_available():
                ok = cdb.upsert_experiment(
                    id=exp_id,
                    hypothesis=hypothesis.strip(),
                    status='running',
                    started_at=exp_start.isoformat(),
                    notes=exp_notes.strip() or None,
                )
                if ok:
                    st.success(f'Experiment {exp_id} logged.')
                    st.rerun()
                else:
                    st.error('Failed to write experiment to database.')
            else:
                st.warning(
                    'SQLite context DB not available. '
                    'Make sure soloos-core is installed: pip install -e .[dashboard]'
                )


# ══════════════════════════════════════════════════════════════════════════════
# Main router
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    page = render_sidebar()

    if page == 'Morning Brief':
        page_morning_brief()
    elif page == 'Decision History':
        page_decision_history()
    elif page == 'KPI Dashboard':
        page_kpi_dashboard()
    elif page == 'Experiments':
        page_experiments()
    else:
        st.error(f'Unknown page: {page}')


main()
