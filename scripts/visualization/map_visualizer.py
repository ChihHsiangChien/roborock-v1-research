#!/usr/bin/env python3
"""
Roborock V1 Map Parser & Visualizer
Valetudo Map to PNG converter
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
import sys
import argparse

def parse_compressed_pixels(compressed):
    """Parse Valetudo compressed pixel format: [x1, y1, count1, x2, y2, count2, ...]"""
    pixels = []
    i = 0
    while i < len(compressed) - 2:
        x = compressed[i]
        y = compressed[i + 1]
        count = compressed[i + 2]
        for _ in range(count):
            pixels.append((x, y))
        i += 3
    return pixels

def create_map_from_layers(layers, map_size):
    """Create map array from layers. 0=unknown, 1=floor, 2=wall"""
    map_data = np.zeros((map_size['y'], map_size['x']), dtype=np.uint8)
    layer_types = {'floor': 1, 'wall': 2}
    
    for layer in layers:
        layer_type = layer.get('type', '')
        compressed = layer.get('compressedPixels', [])
        pixels = parse_compressed_pixels(compressed)
        
        for x, y in pixels:
            if 0 <= x < map_size['x'] and 0 <= y < map_size['y']:
                map_data[y, x] = layer_types.get(layer_type, 1)
    
    return map_data

def parse_entities(entities):
    """Parse map entities (charger, robot, path)"""
    result = {'charger': None, 'robot': None, 'path': []}
    
    for entity in entities:
        entity_type = entity.get('type', '')
        
        if entity_type == 'charger_location':
            points = entity.get('points', [])
            if len(points) >= 2:
                result['charger'] = (points[0], points[1])
        
        elif entity_type == 'robot_position':
            points = entity.get('points', [])
            angle = entity.get('metaData', {}).get('angle', 0)
            if len(points) >= 2:
                result['robot'] = (points[0], points[1], angle)
        
        elif entity_type == 'path':
            points = entity.get('points', [])
            path_points = []
            for i in range(0, len(points) - 1, 2):
                path_points.append((points[i], points[i + 1]))
            result['path'] = path_points
    
    return result

def visualize_map(map_data, entities, pixel_size, output_file=None, show=True):
    """Visualize the map"""
    colors = ['#1a1a1a', '#ffffff', '#888888']  # unknown, floor, wall
    cmap = LinearSegmentedColormap.from_list('map', colors)
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 12))
    
    ax.imshow(map_data, cmap=cmap, origin='lower', aspect='equal')
    
    if entities['charger']:
        x, y = entities['charger']
        ax.plot(x, y, 'g^', markersize=15, label='Charger')
        ax.add_patch(plt.Circle((x, y), 30, fill=False, color='green', linewidth=2))
    
    if entities['robot']:
        x, y, angle = entities['robot']
        ax.plot(x, y, 'ro', markersize=12, label='Robot')
        arrow_len = 50
        dx = arrow_len * np.cos(np.radians(angle))
        dy = arrow_len * np.sin(np.radians(angle))
        ax.arrow(x, y, dx, dy, head_width=20, head_length=10, fc='red', ec='red')
    
    if entities['path']:
        path = np.array(entities['path'])
        if len(path) > 1:
            ax.plot(path[:, 0], path[:, 1], 'b-', linewidth=1, alpha=0.5, label='Path')
    
    # Scale bar
    scale_size = 100
    scale_cm = scale_size * pixel_size
    if scale_cm >= 100:
        scale_text = f"{scale_cm/100:.1f} m"
    else:
        scale_text = f"{scale_cm:.0f} cm"
    
    ax.plot([20, 20 + scale_size], [30, 30], 'w-', linewidth=3)
    ax.text(20 + scale_size/2, 45, scale_text, color='white', ha='center', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='black', alpha=0.7))
    
    ax.set_title(f'Roborock V1 Map (Pixel Size: {pixel_size} cm)', fontsize=14, color='white')
    ax.axis('off')
    
    legend_elements = [
        mpatches.Patch(facecolor='green', label='Charging Dock'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Robot'),
        plt.Line2D([0], [0], color='blue', linewidth=2, label='Path'),
        mpatches.Patch(facecolor='white', label='Floor'),
        mpatches.Patch(facecolor='#888888', label='Wall'),
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=9,
             facecolor='black', edgecolor='white', labelcolor='white')
    
    fig.patch.set_facecolor('#2d2d2d')
    ax.set_facecolor('#1a1a1a')
    
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=150, bbox_inches='tight',
                   facecolor=fig.get_facecolor())
        print(f"Map saved to: {output_file}")
    
    if show:
        plt.show()
    
    return fig, ax

def main():
    parser = argparse.ArgumentParser(description='Roborock V1 Map Visualizer')
    parser.add_argument('input', nargs='?', default='/home/student/robot/map_dump.json')
    parser.add_argument('-o', '--output', default=None)
    parser.add_argument('-s', '--show', action='store_true', default=True)
    parser.add_argument('--no-show', action='store_false', dest='show')
    
    args = parser.parse_args()
    
    print(f"Loading map: {args.input}")
    with open(args.input, 'r') as f:
        data = json.load(f)
    
    map_size = data.get('size', {'x': 5120, 'y': 5120})
    pixel_size = data.get('pixelSize', 5)
    layers = data.get('layers', [])
    entities = data.get('entities', [])
    
    map_data = create_map_from_layers(layers, map_size)
    parsed_entities = parse_entities(entities)
    
    print(f"Map size: {map_data.shape[1]} x {map_data.shape[0]} pixels")
    print(f"Pixel size: {pixel_size} cm")
    
    if parsed_entities['charger']:
        print(f"Charger position: {parsed_entities['charger']}")
    if parsed_entities['robot']:
        print(f"Robot position: {parsed_entities['robot']}")
    if parsed_entities['path']:
        print(f"Path points: {len(parsed_entities['path'])}")
    
    visualize_map(map_data, parsed_entities, pixel_size,
                 output_file=args.output, show=args.show)

if __name__ == '__main__':
    main()
