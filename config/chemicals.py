"""
Chemical properties and data for flame tests
"""

# Chemical flame test data
CHEMICALS = {
    'Na': {
        'name': 'Sodium',
        'formula': 'NaCl',
        'color': (0, 255, 255),  # BGR format - Yellow
        'description': 'Sodium produces a bright yellow flame due to electron transitions in the D-line',
        'safety_warning': 'Sodium compounds are generally safe but can be irritating. Always wear safety goggles.',
        'temperature': 589,  # Wavelength in nm
        'intensity': 0.9,
        'particle_color': (0, 200, 255)
    },
    'K': {
        'name': 'Potassium',
        'formula': 'KCl',
        'color': (255, 0, 128),  # BGR format - Lilac/Purple
        'description': 'Potassium creates a lilac flame due to multiple electron transitions',
        'safety_warning': 'Potassium compounds can be reactive. Handle with care and use proper ventilation.',
        'temperature': 766,  # Wavelength in nm
        'intensity': 0.7,
        'particle_color': (200, 0, 255)
    },
    'Li': {
        'name': 'Lithium',
        'formula': 'LiCl',
        'color': (0, 0, 255),  # BGR format - Crimson Red
        'description': 'Lithium produces a crimson red flame from electron transitions in the metal atom',
        'safety_warning': 'Lithium compounds are generally safe but can cause skin irritation.',
        'temperature': 670,  # Wavelength in nm
        'intensity': 0.8,
        'particle_color': (0, 100, 255)
    },
    'Cu': {
        'name': 'Copper',
        'formula': 'CuSO₄',
        'color': (128, 255, 0),  # BGR format - Blue-green
        'description': 'Copper produces blue-green flames due to electron transitions in copper ions',
        'safety_warning': 'Copper compounds can be toxic. Avoid inhalation and skin contact.',
        'temperature': 515,  # Wavelength in nm
        'intensity': 0.85,
        'particle_color': (200, 255, 100)
    },
    'Ca': {
        'name': 'Calcium',
        'formula': 'CaCl₂',
        'color': (0, 127, 255),  # BGR format - Orange-red
        'description': 'Calcium creates an orange-red flame from electron transitions in calcium atoms',
        'safety_warning': 'Calcium compounds are generally safe but can cause eye irritation.',
        'temperature': 622,  # Wavelength in nm
        'intensity': 0.75,
        'particle_color': (0, 150, 255)
    },
    'Ba': {
        'name': 'Barium',
        'formula': 'BaCl₂',
        'color': (0, 255, 128),  # BGR format - Pale green
        'description': 'Barium produces a pale green flame due to electron transitions in barium ions',
        'safety_warning': 'CAUTION: Barium compounds are toxic. Avoid inhalation and ingestion.',
        'temperature': 554,  # Wavelength in nm
        'intensity': 0.6,
        'particle_color': (100, 255, 200)
    }
}

# Chemical mixing reactions
CHEMICAL_MIXTURES = {
    ('Na', 'K'): {
        'result_color': (128, 128, 255),  # Yellow-purple mix
        'description': 'Sodium and Potassium create a mixed yellow-purple flame with alternating colors',
        'explanation': 'Both elements emit simultaneously, creating a flickering effect between yellow and purple',
        'realistic_note': 'In reality, the stronger sodium yellow often dominates the weaker potassium purple'
    },
    ('Li', 'Cu'): {
        'result_color': (64, 128, 255),  # Red-blue mix
        'description': 'Lithium and Copper create a reddish-blue flame with purple tints',
        'explanation': 'The combination creates intermediate wavelengths between red and blue-green',
        'realistic_note': 'Real mixtures often show both colors distinctly rather than blending'
    },
    ('Ca', 'Ba'): {
        'result_color': (0, 191, 191),  # Orange-green mix
        'description': 'Calcium and Barium create a yellow-green flame with orange highlights',
        'explanation': 'The orange-red of calcium blends with the pale green of barium',
        'realistic_note': 'Mixed flames often flicker between the two distinct colors'
    },
    ('Na', 'Cu'): {
        'result_color': (64, 255, 128),  # Yellow-blue mix
        'description': 'Sodium and Copper create a bright green flame with yellow edges',
        'explanation': 'Yellow sodium light combines with blue-green copper to create green',
        'realistic_note': 'This is one of the more visually appealing realistic mixtures'
    },
    ('K', 'Ca'): {
        'result_color': (128, 64, 191),  # Purple-orange mix
        'description': 'Potassium and Calcium create a reddish-purple flame',
        'explanation': 'The lilac of potassium blends with the orange-red of calcium',
        'realistic_note': 'Mixed flame often shows distinct regions of each color'
    },
    ('Li', 'Ba'): {
        'result_color': (0, 128, 255),  # Red-green mix
        'description': 'Lithium and Barium create a unique brownish-red flame with green tinges',
        'explanation': 'Red lithium mixed with green barium creates intermediate brown colors',
        'realistic_note': 'This mixture often appears muddy in real flame tests'
    }
}

# Beaker positions (relative to screen width) - REMOVED Ba, moved Water to top-right
BEAKER_POSITIONS = {
    'Na': 0.08,   # 8% from left
    'K': 0.22,    # 22% from left  
    'Li': 0.36,   # 36% from left
    'Cu': 0.50,   # 50% from left
    'Ca': 0.64,   # 64% from left
    # Ba removed to prevent overlap
    # Water moved to top-right corner
}

# Water beaker position (top-center)
WATER_POSITION = {
    'x_ratio': 0.5,   # 50% from left (center)
    'y_ratio': 0.12   # 12% from top
}

# Flame ignition area (relative to screen)
FLAME_AREA = {
    'x': 0.05,  # 5% from left
    'y': 0.3,   # 30% from top
    'width': 0.1,  # 10% of screen width
    'height': 0.2  # 20% of screen height
}

# Visual constants - OPTIMIZED FOR HIGH FPS
BEAKER_SIZE = 90  # Increased from 80
FLAME_SIZE = 120  # Increased from 60 - BIGGER FLAMES!
INTERACTION_RADIUS = 45  # Slightly increased
PARTICLE_LIFETIME = 40   # Reduced from 60 for better performance
FPS_TARGET = 120         # Target 120+ FPS
MAX_PARTICLES = 150      # Reduced from 200 for performance

# Educational content
FLAME_TEST_THEORY = """
Flame tests work because when metal atoms are heated, their electrons absorb energy and move to higher energy levels. 
When these electrons return to their ground state, they emit light at specific wavelengths, creating characteristic colors.
Each element has a unique electron configuration, resulting in unique flame colors.
"""