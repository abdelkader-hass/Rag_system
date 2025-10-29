import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
import os
import random

# Professional styling configuration
st.set_page_config(
    page_title="Device Ticket Analytics",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional appearance
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background-color: #f8fafc;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3b82f6;
        margin-bottom: 1rem;
    }
    .category-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #374151;
        margin-bottom: 0.75rem;
    }
    .stButton>button {
        background-color: #3b82f6;
        color: white;
        font-weight: 500;
        border-radius: 0.375rem;
        padding: 0.5rem 2rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #2563eb;
    }
    </style>
""", unsafe_allow_html=True)

# Header section
st.markdown('<p class="main-header">Device Ticket Analytics Dashboard</p>', unsafe_allow_html=True)
st.markdown("**Comprehensive ticket tracking and resolution analysis**")
st.divider()

# Configuration section
col_config1, col_config2, col_config3 = st.columns([2, 2, 1])

with col_config1:
    device_input = st.text_input(
        "Device Names",
        "emission,raman",
        help="Enter comma-separated device names"
    )

with col_config2:
    devices = [d.strip() for d in device_input.split(",") if d.strip()]
    selected_device = st.selectbox(
        "Select Device",
        devices,
        help="Choose a device to analyze"
    )

with col_config3:
    st.write("")
    st.write("")
    show_stats = st.button("Generate Report", use_container_width=True)

if show_stats:
    csv_path = f"{selected_device}_qrqc_data.csv"

    if not os.path.exists(csv_path):
        st.error(f"⚠️ Data file not found: {csv_path}")
    else:
        df = pd.read_csv(csv_path)

        # Data preview section
        with st.expander("📋 View Raw Data", expanded=False):
            st.caption(f"Source: {selected_device}_data.csv")
            tab1, tab2 = st.tabs(["First Records", "Latest Records"])
            with tab1:
                st.dataframe(df.head(), use_container_width=True)
            with tab2:
                st.dataframe(df.tail(), use_container_width=True)

        st.divider()

        # Discussion detection logic
        discussion_columns = ["notes", "QR PROD"]

        def has_discussion(row):
            for col in discussion_columns:
                if col in row and pd.notna(row[col]) and str(row[col]).strip():
                    return True
            return False

        df["has_discussion"] = df.apply(has_discussion, axis=1)

        # Normalize solved status
        df["solved"] = False

        # ✅ Case 1: Check "Problème résolu ?"
        if "Problème résolu ?" in df.columns:
            df["solved"] = df["Problème résolu ?"].isin([1, "1", True, "True", "true"])

        # ✅ Case 2: Check "solution" column if it exists and not empty
        if "*QR* Solution QR" in df.columns:
            # Mark as True if solution column is not null/empty
            df.loc[df["*QR* Solution QR"].notna() & (df["*QR* Solution QR"].astype(str).str.strip() != ""), "solved"] = True

        # Category definitions
        categories = {
            "Discussion + Resolved": df[(df["has_discussion"]) & (df["solved"])],
            "Discussion + Unresolved": df[(df["has_discussion"]) & (~df["solved"])],
            "No Discussion + Resolved": df[(~df["has_discussion"]) & (df["solved"])],
            "No Discussion + Unresolved": df[(~df["has_discussion"]) & (~df["solved"])],
        }

        # Key metrics overview
        st.subheader("Executive Summary")
        metric_cols = st.columns(4)
        
        total_tickets = len(df)
        total_resolved = len(df[df["solved"]])
        resolution_rate = (total_resolved / total_tickets * 100) if total_tickets > 0 else 0
        tickets_with_discussion = len(df[df["has_discussion"]])

        metric_cols[0].metric("Total Tickets", f"{total_tickets:,}")
        metric_cols[1].metric("Resolved", f"{total_resolved:,}")
        metric_cols[2].metric("Resolution Rate", f"{resolution_rate:.1f}%")
        metric_cols[3].metric("With Discussion", f"{tickets_with_discussion:,}")

        st.divider()

        # Detailed breakdown
        st.subheader(f"Detailed Analysis – {selected_device.title()}")

        # Find instrument type column
        type_col = next(
            (c for c in df.columns
             if any(keyword.lower() in c.lower() 
                   for keyword in ["type instrument", "type d'instrument"])),
            None
        )

        col_left, col_right = st.columns(2)

        for idx, (name, subset) in enumerate(categories.items()):
            col = col_left if idx % 2 == 0 else col_right
            count = len(subset)
            
            with col:
                st.markdown(f"#### {name}")
                st.metric("Ticket Count", count)

                # Module type breakdown
                if type_col and not subset.empty and type_col in subset.columns:
                    type_counts = subset[type_col].value_counts()
                    st.markdown("**Module Distribution:**")
                    for module_type, module_count in type_counts.items():
                        percentage = (module_count / count * 100) if count > 0 else 0
                        st.write(f"• {module_type}: {module_count} ({percentage:.1f}%)")
                else:
                    st.caption("No module type data available")

                # Sample ticket IDs
                if "ticket_id" in subset.columns and count > 0:
                    sample_ids = random.sample(subset["ticket_id"].tolist(), min(2, count))
                    st.markdown("**Sample Tickets:**")
                    for ticket_id in sample_ids:
                        st.markdown(f"[#{ticket_id}](http://hfrredmine.jy.fr/issues/{ticket_id})")
                
                st.markdown("---")

        # Visualization
        st.divider()
        st.subheader("Visual Summary")
        
        fig, ax = plt.subplots(figsize=(10, 5))
        colors = ['#10b981', '#ef4444', '#3b82f6', '#f59e0b']
        bars = ax.bar(
            range(len(categories)),
            [len(v) for v in categories.values()],
            color=colors,
            edgecolor='#1f2937',
            linewidth=1.5
        )
        
        ax.set_title(
            f"Ticket Distribution – {selected_device.title()}",
            fontsize=14,
            fontweight='600',
            pad=20
        )
        ax.set_ylabel("Number of Tickets", fontsize=11, fontweight='500')
        ax.set_xticks(range(len(categories)))
        ax.set_xticklabels(
            [k.replace(" + ", "\n") for k in categories.keys()],
            fontsize=9,
            ha="center"
        )
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2.,
                height,
                f'{int(height)}',
                ha='center',
                va='bottom',
                fontweight='600'
            )
        
        plt.tight_layout()
        st.pyplot(fig)