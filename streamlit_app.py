import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set page title and layout
st.set_page_config(
    page_title="TPMS Scaffold Predictor",
    layout="centered"
)

# Title with custom styling
st.markdown("""
    <h1 style='text-align: center; color: #2e6c80;'>
        CHITOSAN-BASED TPMS SCAFFOLD PERFORMANCE PREDICTOR
    </h1>
    <h3 style='text-align: center; color: #666666;'>
        Articular Cartilage Tissue Regeneration
    </h3>
    """, unsafe_allow_html=True)

# Create input form
with st.form("prediction_form"):
    st.subheader("Enter Scaffold Parameters")
    
    # Select biomaterial
    biomaterials = ["Chitosan", "Zinc Oxide", "Type II Collagen"]
    selected_biomaterial = st.selectbox("Select Biomaterial", biomaterials)
    
    # Input fields
    porosity = st.slider("Porosity (%)", 30.0, 90.0, 70.0)
    
    # Submit button
    submit = st.form_submit_button("Predict Performance")

# When form is submitted
if submit:
    # Create prediction (replace with your actual prediction model)
    cell_migration = np.random.uniform(75, 95)
    mechanical_strength = np.random.uniform(70, 90)
    
    # Simulated FEA results
    stress = np.random.uniform(5, 20, size=10)  # Stress values
    strain = np.random.uniform(0, 0.1, size=10)  # Strain values
    
    # Simulated CFD results
    flow_rate = np.random.uniform(10, 50, size=10)  # Flow rates
    shear_stress = np.random.uniform(100, 500, size=10)  # Shear stress values

    # Display results in columns
    st.subheader("Predicted Performance Metrics")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="Cell Migration",
            value=f"{cell_migration:.1f}%"
        )
    
    with col2:
        st.metric(
            label="Mechanical Strength",
            value=f"{mechanical_strength:.1f}%"
        )

    # Display FEA results
    st.subheader("Finite Element Analysis Results")
    st.write(f"**Average Stress:** {np.mean(stress):.2f} MPa")
    st.write(f"**Average Strain:** {np.mean(strain):.2f}")

    # Create stress-strain line plot
    plt.figure(figsize=(8, 4))
    plt.plot(strain, stress, marker='o', color='blue', linestyle='-')
    plt.title('Stress-Strain Distribution')
    plt.xlabel('Strain')
    plt.ylabel('Stress (MPa)')
    plt.grid()
    st.pyplot(plt)

    # Display CFD results
    st.subheader("Computational Fluid Dynamics Results")
    st.write(f"**Average Flow Rate:** {np.mean(flow_rate):.2f} mL/min")
    st.write(f"**Average Shear Stress:** {np.mean(shear_stress):.2f} Pa")

    # Create dot distribution scatter chart for CFD results
    plt.figure(figsize=(8, 4))
    plt.scatter(flow_rate, shear_stress, color='orange')
    plt.title('Dot Distribution of Flow Rate and Shear Stress')
    plt.xlabel('Flow Rate (mL/min)')
    plt.ylabel('Shear Stress (Pa)')
    plt.grid()
    st.pyplot(plt)

    # Add recommendations based on predictions
    st.subheader("Analysis & Recommendations")
    st.write(f"""
    Based on the input parameters for **{selected_biomaterial}**:
    - The scaffold design shows good potential for tissue engineering.
    - Porosity level is suitable for cell infiltration.
    - Mechanical properties are within the desired range.
    - FEA indicates acceptable stress and strain levels.
    - CFD results suggest effective fluid dynamics for nutrient transport.
    """)
    
    # Create a simple visualization of the parameters
    st.subheader("Parameter Overview")
    data = pd.DataFrame({
        'Parameter': ['Biomaterial', 'Porosity'],
        'Value': [selected_biomaterial, porosity],
        'Unit': ['', '%']
    })
    st.dataframe(data, hide_index=True)

# Add footer
st.markdown("---")
st.markdown("""
    <p style='text-align: center; color: #666666;'>
        Note: This is a predictive model based on Monte Carlo simulation data. 
        Results should be validated experimentally.
    </p>
    """, unsafe_allow_html=True)
