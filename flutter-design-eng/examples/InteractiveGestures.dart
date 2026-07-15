import 'package:flutter/physics.dart';
import 'package:flutter/widgets.dart';

class PhysicsCardDraggable extends StatefulWidget {
  final Widget child;
  const PhysicsCardDraggable({required this.child, super.key});

  @override
  State<PhysicsCardDraggable> createState() => _PhysicsCardDraggableState();
}

class _PhysicsCardDraggableState extends State<PhysicsCardDraggable>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController.unbounded(vsync: this);
  }

  void _runSpringSimulation(double velocityY) {
    final spring = SpringDescription(mass: 1.0, stiffness: 120, damping: 12);
    final simulation = SpringSimulation(spring, _controller.value, 0.0, velocityY);
    _controller.animateWith(simulation);
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    
    return GestureDetector(
      onPanDown: (_) => _controller.stop(),
      onPanUpdate: (details) {
        _controller.value += details.delta.dy / (size.height / 2);
      },
      onPanEnd: (details) {
        final velocityY = details.velocity.pixelsPerSecond.dy / (size.height / 2);
        _runSpringSimulation(velocityY);
      },
      child: AnimatedBuilder(
        animation: _controller,
        child: widget.child,
        builder: (context, child) {
          return Align(
            alignment: Alignment(0, _controller.value),
            child: child,
          );
        },
      ),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }
}
