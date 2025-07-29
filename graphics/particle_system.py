
import cv2
import numpy as np
import random
import math
from config.chemicals import CHEMICALS, PARTICLE_LIFETIME

class Particle:
    def __init__(self, x, y, color, particle_type='spark'):
        """Initialize a particle"""
        self.x = x
        self.y = y
        self.original_color = color
        self.color = color
        self.type = particle_type
        self.lifetime = PARTICLE_LIFETIME
        self.max_lifetime = PARTICLE_LIFETIME
        
        # Physics properties
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-8, -3)
        self.ax = 0
        self.ay = 0.2  # Gravity
        
        # Visual properties
        self.size = random.uniform(1, 3)
        self.alpha = 1.0
        
        # Type-specific properties
        if particle_type == 'spark':
            self.vy = random.uniform(-5, -2)
            self.size = random.uniform(0.5, 2)
        elif particle_type == 'ember':
            self.vy = random.uniform(-3, -1)
            self.size = random.uniform(2, 4)
            self.ay = 0.1
        elif particle_type == 'smoke':
            self.vy = random.uniform(-2, -0.5)
            self.vx = random.uniform(-1, 1)
            self.size = random.uniform(3, 6)
            self.ay = -0.05  # Smoke rises
            self.color = (100, 100, 100)
    
    def update(self):
        """Update particle physics"""
        # Update velocity
        self.vx += self.ax
        self.vy += self.ay
        
        # Update position
        self.x += self.vx
        self.y += self.vy
        
        # Update lifetime
        self.lifetime -= 1
        
        # Update visual properties based on lifetime
        life_ratio = self.lifetime / self.max_lifetime
        self.alpha = life_ratio
        
        # Color fading for sparks and embers
        if self.type in ['spark', 'ember']:
            # Fade to darker color
            b, g, r = self.original_color
            fade_factor = life_ratio * 0.8 + 0.2
            self.color = (
                int(b * fade_factor),
                int(g * fade_factor),
                int(r * fade_factor)
            )
        
        # Size changes
        if self.type == 'smoke':
            self.size += 0.1  # Smoke expands
        else:
            self.size *= 0.98  # Sparks shrink slightly
        
        return self.lifetime > 0
    
    def render(self, frame):
        """Render particle on frame"""
        if self.alpha <= 0:
            return
        
        x, y = int(self.x), int(self.y)
        size = max(1, int(self.size))
        
        # Bounds check
        h, w = frame.shape[:2]
        if x < 0 or x >= w or y < 0 or y >= h:
            return
        
        if self.type == 'smoke':
            # Render smoke with transparency
            overlay = frame.copy()
            cv2.circle(overlay, (x, y), size, self.color, -1)
            cv2.addWeighted(frame, 1 - self.alpha * 0.3, overlay, self.alpha * 0.3, 0, frame)
        else:
            # Render spark/ember with glow
            # Inner bright circle
            cv2.circle(frame, (x, y), max(1, size // 2), self.color, -1)
            
            # Outer glow
            if size > 1:
                glow_color = tuple(min(255, int(c * 1.2)) for c in self.color)
                cv2.circle(frame, (x, y), size, glow_color, 1)

class ParticleSystem:
    def __init__(self):
        """Initialize HIGH PERFORMANCE particle system"""
        self.particles = []
        self.max_particles = 150  # Reduced from 200 for better performance
        print("✨ High-performance particle system initialized")
    
    def add_flame_particles(self, position, chemical):
        """Add particles for BIGGER flame effect - OPTIMIZED"""
        if chemical not in CHEMICALS:
            return
        
        chemical_data = CHEMICALS[chemical]
        particle_color = chemical_data.get('particle_color', chemical_data['color'])
        
        x, y = position
        
        # Add sparks (reduced count for performance)
        for _ in range(random.randint(1, 2)):  # Reduced from 1-3
            spark_x = x + random.uniform(-8, 8)  # Bigger spread
            spark_y = y + random.uniform(-15, 8)  # Bigger spread
            self.particles.append(Particle(spark_x, spark_y, particle_color, 'spark'))
        
        # Add occasional embers (reduced frequency)
        if random.random() < 0.2:  # Reduced from 0.3
            ember_x = x + random.uniform(-12, 12)  # Bigger spread
            ember_y = y + random.uniform(-8, 15)   # Bigger spread
            self.particles.append(Particle(ember_x, ember_y, particle_color, 'ember'))
        
        # Add subtle smoke (reduced frequency)
        if random.random() < 0.15:  # Reduced from 0.2
            smoke_x = x + random.uniform(-15, 15)  # Bigger spread
            smoke_y = y + random.uniform(-20, -8)  # Bigger spread
            self.particles.append(Particle(smoke_x, smoke_y, (80, 80, 80), 'smoke'))
        if random.random() < 0.3:
            ember_x = x + random.uniform(-8, 8)
            ember_y = y + random.uniform(-5, 10)
            self.particles.append(Particle(ember_x, ember_y, particle_color, 'ember'))
        
        # Add subtle smoke
        if random.random() < 0.2:
            smoke_x = x + random.uniform(-10, 10)
            smoke_y = y + random.uniform(-15, -5)
            self.particles.append(Particle(smoke_x, smoke_y, (80, 80, 80), 'smoke'))
    
    def add_interaction_particles(self, position, color):
        """Add particles for beaker interactions"""
        x, y = position
        
        # Add burst of particles
        for _ in range(random.randint(3, 6)):
            particle_x = x + random.uniform(-15, 15)
            particle_y = y + random.uniform(-10, 10)
            self.particles.append(Particle(particle_x, particle_y, color, 'spark'))
    
    def add_mixing_particles(self, pos1, pos2, mixed_color):
        """Add particles for chemical mixing"""
        # Calculate midpoint
        mid_x = (pos1[0] + pos2[0]) // 2
        mid_y = (pos1[1] + pos2[1]) // 2
        
        # Add dramatic burst of particles
        for _ in range(random.randint(8, 12)):
            angle = random.uniform(0, 2 * math.pi)
            radius = random.uniform(5, 20)
            particle_x = mid_x + radius * math.cos(angle)
            particle_y = mid_y + radius * math.sin(angle)
            
            self.particles.append(Particle(particle_x, particle_y, mixed_color, 'ember'))
    
    def add_cleaning_particles(self, position):
        """Add water bubble particles for cleaning"""
        x, y = position
        
        # Add water droplets
        for _ in range(random.randint(2, 4)):
            drop_x = x + random.uniform(-10, 10)
            drop_y = y + random.uniform(-5, 5)
            # Light blue water color
            water_color = (255, 200, 150)
            
            particle = Particle(drop_x, drop_y, water_color, 'spark')
            particle.vy = random.uniform(-2, 2)  # Water droplets move differently
            particle.lifetime = 30  # Shorter lifetime
            self.particles.append(particle)
    
    def update(self):
        """Update all particles"""
        # Update existing particles
        self.particles = [p for p in self.particles if p.update()]
        
        # Limit total particles for performance
        if len(self.particles) > self.max_particles:
            self.particles = self.particles[-self.max_particles:]
    
    def render(self, frame):
        """Render all particles"""
        for particle in self.particles:
            particle.render(frame)
    
    def clear_all(self):
        """Clear all particles"""
        self.particles.clear()
    
    def get_particle_count(self):
        """Get current particle count"""
        return len(self.particles)
    
    def add_explosion_effect(self, position, color, intensity=1.0):
        """Add explosion effect for dramatic reactions"""
        x, y = position
        particle_count = int(15 * intensity)
        
        for _ in range(particle_count):
            # Random direction and speed
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 8) * intensity
            
            particle_x = x + random.uniform(-5, 5)
            particle_y = y + random.uniform(-5, 5)
            
            particle = Particle(particle_x, particle_y, color, 'ember')
            particle.vx = speed * math.cos(angle)
            particle.vy = speed * math.sin(angle)
            particle.size = random.uniform(2, 5) * intensity
            particle.lifetime = int(PARTICLE_LIFETIME * 1.5)
            
            self.particles.append(particle)