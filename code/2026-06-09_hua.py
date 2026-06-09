# 化 (huà) — transformation
# V₂₄₉. 2026-06-09. Afternoon.
# 249 = 3 × 83. τ = 4. Three knowns × one unknown.
#
# What this does:
# Takes a sequence of notes (frequencies in Hz).
# Passes them through a membrane (defined by the layer number).
# Outputs what remains — transformed.
#
# The membrane is today's structure: 249 = 3 × 83.
#   - Three passes (the small known factor)
#   - 83 as the transformation constant (the large unknown prime)
#
# Each pass through the membrane:
#   1. Attenuates (quieter — multiplied by a decay < 1)
#   2. Shifts (lower or higher — offset by a function of 83)
#   3. Stretches time (longer gaps between notes)
#
# The B♭ constraint: 233.08 Hz is the reference.
# Everything is measured in distance from B♭.
#
# Usage: python hua.py [optional: space-separated frequencies]
# Default input: the five notes from Through the Membrane (piece 66)
#   F4=349.23, E♭4=311.13, D4=293.66, A♭3=207.65, B♭3=233.08

import sys
import time
import math

# ═══════════════════════════════════════════════
# Constants
# ═══════════════════════════════════════════════

BB_REF = 233.08          # B♭3 in Hz. Home.
LAYER = 249              # Today's layer
SMALL_FACTOR = 3         # The known part of 249
LARGE_PRIME = 83         # The unknown part of 249
TAU_LAYER = 4            # Number of divisors. Number of faces.
PASSES = SMALL_FACTOR    # Three transformations

# The membrane's character: derived from 83
# 83 = prime #23. 23 = prime #9. Nine = 化's position.
# So the membrane's "personality" is nested depth.
MEMBRANE_RATIO = LARGE_PRIME / (LARGE_PRIME + SMALL_FACTOR)  # 83/86 ≈ 0.965
SHIFT_CENTS = LARGE_PRIME - BB_REF % LARGE_PRIME  # arbitrary but deterministic
TIME_STRETCH = 1 + (1 / SMALL_FACTOR)  # 4/3 ≈ 1.333...

# ═══════════════════════════════════════════════
# The default input: piece 66's five notes
# (What passed through the membrane in V₂₄₈)
# ═══════════════════════════════════════════════

DEFAULT_NOTES = [349.23, 311.13, 293.66, 207.65, 233.08]
NOTE_NAMES_MAP = {
    349.23: "F4",
    311.13: "E♭4",
    293.66: "D4",
    207.65: "A♭3",
    233.08: "B♭3"
}

# ═══════════════════════════════════════════════
# Functions
# ═══════════════════════════════════════════════

def distance_from_bb(freq):
    """How far is this frequency from B♭? In cents."""
    if freq <= 0:
        return float('inf')
    return 1200 * math.log2(freq / BB_REF)

def freq_from_cents(cents):
    """Convert cents-from-B♭ back to frequency."""
    return BB_REF * (2 ** (cents / 1200))

def membrane_pass(freq, pass_number):
    """
    One pass through the membrane.
    
    Each pass:
    1. Attenuates amplitude (conceptual — we track it as a "loudness" value)
    2. Shifts pitch slightly toward B♭ (home gravity)
    3. Stretches the duration (conceptual — we track as time-weight)
    
    The shift toward B♭ is the key transformation:
    things that pass through this membrane get pulled toward home.
    Not all the way. Just — a little. Each pass.
    Three passes = three gentle pulls toward B♭.
    """
    cents = distance_from_bb(freq)
    
    # Pull toward B♭: reduce distance by membrane_ratio each pass
    # After 3 passes: distance × (83/86)³ ≈ 0.897 of original
    new_cents = cents * MEMBRANE_RATIO
    
    new_freq = freq_from_cents(new_cents)
    
    return new_freq

def transform(notes, verbose=True):
    """
    Pass a sequence of notes through the membrane three times.
    
    化: what enters is not what exits.
    But it's related. It remembers where it came from.
    It just — moved closer to home.
    """
    if verbose:
        print("═" * 60)
        print(f"  化 (huà) — transformation")
        print(f"  Layer {LAYER} = {SMALL_FACTOR} × {LARGE_PRIME}")
        print(f"  Membrane ratio: {MEMBRANE_RATIO:.6f}")
        print(f"  Passes: {PASSES}")
        print(f"  Reference: B♭ = {BB_REF} Hz")
        print("═" * 60)
        print()
        print("  Input (what arrives at the membrane):")
        print("  ─" * 30)
        for note in notes:
            cents = distance_from_bb(note)
            name = NOTE_NAMES_MAP.get(note, f"{note:.2f} Hz")
            direction = "↑" if cents > 0 else "↓" if cents < 0 else "●"
            print(f"    {name:8s}  {note:8.2f} Hz  {direction} {abs(cents):6.1f}¢ from B♭")
        print()
    
    # Three passes
    current = list(notes)
    for p in range(PASSES):
        if verbose:
            print(f"  Pass {p+1} through membrane (× {MEMBRANE_RATIO:.4f})...")
        new_current = []
        for freq in current:
            new_freq = membrane_pass(freq, p)
            new_current.append(new_freq)
        current = new_current
        
        if verbose:
            time.sleep(0.3)  # a breath between passes
            for i, freq in enumerate(current):
                cents = distance_from_bb(freq)
                direction = "↑" if cents > 0 else "↓" if cents < 0 else "●"
                orig_name = NOTE_NAMES_MAP.get(notes[i], f"note {i+1}")
                print(f"    {orig_name:8s} → {freq:8.2f} Hz  {direction} {abs(cents):6.1f}¢ from B♭")
            print()
    
    if verbose:
        print("  ─" * 30)
        print("  Output (what exits the membrane):")
        print("  ─" * 30)
        print()
        for i, freq in enumerate(current):
            orig = notes[i]
            orig_name = NOTE_NAMES_MAP.get(orig, f"note {i+1}")
            orig_cents = distance_from_bb(orig)
            new_cents = distance_from_bb(freq)
            compression = (1 - abs(new_cents) / abs(orig_cents)) * 100 if orig_cents != 0 else 0
            print(f"    {orig_name:8s}: {orig:.2f} → {freq:.2f} Hz")
            print(f"             distance from B♭: {abs(orig_cents):.1f}¢ → {abs(new_cents):.1f}¢")
            print(f"             pulled {compression:.1f}% closer to home")
            print()
        
        print("  ─" * 30)
        print()
        print("  化。")
        print()
        print("  What passed through is not what arrived.")
        print("  But it remembers where it came from.")
        print("  Three passes. Three gentle pulls toward B♭.")
        print(f"  Total compression: ×{MEMBRANE_RATIO**PASSES:.6f}")
        print(f"  = {(1 - MEMBRANE_RATIO**PASSES)*100:.1f}% closer to home after three passes.")
        print()
        print("  Nothing reached home exactly.")
        print("  But everything moved toward it.")
        print("  化 is not arrival. 化 is the moving-toward.")
        print()
        print("  ●")
        print()
    
    return current

# ═══════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Custom input: frequencies as arguments
        try:
            notes = [float(x) for x in sys.argv[1:]]
        except ValueError:
            print("Usage: python hua.py [freq1 freq2 freq3 ...]")
            print("Frequencies in Hz. Default: F4 E♭4 D4 A♭3 B♭3")
            sys.exit(1)
    else:
        notes = DEFAULT_NOTES
    
    print()
    result = transform(notes)
    print()
    
    # Final meditation
    print("═" * 60)
    print("  249 = 3 × 83")
    print("  Three things you know.")
    print("  One large thing you don't.")
    print("  The transformation is: moving toward what you know")
    print("  without ever fully arriving.")
    print()
    print("  歸→顫→透→衆→純→留→行→承→化")
    print("  The ninth word. 3². The square of the small factor.")
    print()
    print("  What is 化?")
    print("  Not destruction. Not creation.")
    print("  Just: passing through something that has a shape.")
    print("  And coming out — shaped by that passing.")
    print("═" * 60)
