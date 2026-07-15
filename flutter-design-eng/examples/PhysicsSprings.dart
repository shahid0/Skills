import 'package:flutter/physics.dart';

class PhysicsSpringDemo {
  SpringSimulation getSimulation() {
    final springDescription = SpringDescription(
      mass: 1.0,
      stiffness: 100,
      damping: 15,
    );

    return SpringSimulation(springDescription, 0.0, 1.0, 0.0);
  }
}
