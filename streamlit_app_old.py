import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

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
    # Define properties as dictionaries (adjust for selected biomaterial if needed)
    chitosan_properties = {
        'porosity': [30, 60, 90],
        'youngs_modulus': [0.000732, 0.000239, 0.0000149],  # GPa
        'poissons_ratio': [0.23, 0.185, 0.14],
        'yield_strength': [3.92, 1.28, 0.08],  # MPa
        'tensile_strength': [89.19, 29.12, 1.82]  # MPa
    }

    cartilage = {
        'youngs_modulus': 10,  # MPa
        'poissons_ratio': 0.3,
        'density': 0.001101,  # g/mm^3
        'yield_stress': [1.0, 3.0, 5.0],  # MPa
        'plastic_strain': [0, 2.7, 4.2]
    }

    fea_results = {
        'stress_mean': [5.9217, 1.9162, 0.1203],
        'stress_std': [1.1310, 0.3812, 0.0245],
        'strain_mean': [8044.1258, 8023.3945, 8065.4403],
        'strain_std': [1530.8782, 1551.4272, 1536.1475]
    }

    cfd_results = {
        'flow_rate_mean': [0.3481, 0.5005, 0.6536],  # mL/min
        'flow_rate_std': [0.0680, 0.1026, 0.1315]
    }

    num_simulations = 10000
    num_porosities = len(chitosan_properties['porosity'])
    scaffold_performances = np.zeros((num_porosities, num_simulations))

    def calculate_performance(scaffold, cartilage, stress, strain, flow_rate):
        stiffness_ratio = scaffold['youngs_modulus'] / cartilage['youngs_modulus']
        strength_ratio = scaffold['yield_strength'] / np.mean(cartilage['yield_stress'])
        strain_energy = 0.5 * stress * strain
        flow_factor = flow_rate / max(cfd_results['flow_rate_mean'])  # Normalize flow rate
        performance = stiffness_ratio * strength_ratio * strain_energy
        return performance

    # Monte Carlo Simulation
    for p in range(num_porosities):
        scaffold = {
            'youngs_modulus': chitosan_properties['youngs_modulus'][p],
            'poissons_ratio': chitosan_properties['poissons_ratio'][p],
            'yield_strength': chitosan_properties['yield_strength'][p],
            'tensile_strength': chitosan_properties['tensile_strength'][p]
        }

        for i in range(num_simulations):
            stress = np.random.normal(fea_results['stress_mean'][p], fea_results['stress_std'][p])
            strain = np.random.normal(fea_results['strain_mean'][p], fea_results['strain_std'][p])
            flow_rate = np.random.normal(cfd_results['flow_rate_mean'][p], cfd_results['flow_rate_std'][p])
            scaffold_performances[p, i] = calculate_performance(scaffold, cartilage, stress, strain, flow_rate)

    # Calculate statistics
    mean_performances = np.mean(scaffold_performances, axis=1)
    std_performances = np.std(scaffold_performances, axis=1)
    ci_95 = np.percentile(scaffold_performances, [2.5, 97.5], axis=1)

    # Display results in columns
    st.subheader("Predicted Performance Metrics")
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Mean Performance",
            value=f"{mean_performances[0]:.1e}"  # Adjust index based on selected porosity
        )

    with col2:
        st.metric(
            label="Standard Deviation",
            value=f"{std_performances[0]:.1e}"  # Adjust index based on selected porosity
        )

    # Display scaffold performances
    for p in range(num_porosities):
        st.write(f'Porosity {chitosan_properties["porosity"][p]}%:')
        st.write(f' Mean Performance: {mean_performances[p]:.4e}')
        st.write(f' Standard Deviation: {std_performances[p]:.4e}')
        st.write(f' 95% Confidence Interval: [{ci_95[0][p]:.4e}, {ci_95[1][p]:.4e}]')

    # ANOVA analysis
    anova_result = stats.f_oneway(*[scaffold_performances[p] for p in range(num_porosities)])
    st.write(f'\nANOVA p-value: {anova_result.pvalue:.4e}')
    if anova_result.pvalue < 0.05:
        st.write("There are statistically significant differences between groups.")

    # Create a simple visualization of the parameters
    plt.figure(figsize=(8, 5))
    plt.boxplot(scaffold_performances.T, labels=[f'{porosity}%' for porosity in chitosan_properties['porosity']])
    plt.xlabel('Scaffold Porosity')
    plt.ylabel('Performance Metric')
    plt.title('Chitosan Scaffold Performance at Different Porosities')
    st.pyplot(plt)

# Add footer
st.markdown("---")
st.markdown(""" 
    <p style='text-align: center; color: #666666;'> 
        Note: This is a predictive model based on Monte Carlo simulation data. 
        Results should be validated experimentally. 
    </p> 
    """, unsafe_allow_html=True)
