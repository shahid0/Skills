import 'package:flutter/widgets.dart';

class PerformanceOptimizedDemo extends StatefulWidget {
  const PerformanceOptimizedDemo({super.key});

  @override
  State<PerformanceOptimizedDemo> createState() => _PerformanceOptimizedDemoState();
}

class _PerformanceOptimizedDemoState extends State<PerformanceOptimizedDemo>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 2),
    )..repeat(reverse: true);
  }

  @override
  Widget build(BuildContext context) {
    return Center(
      child: RepaintBoundary(
        child: AnimatedBuilder(
          animation: _controller,
          child: const ExpensiveStaticCard(),
          builder: (context, child) {
            return Transform.rotate(
              angle: _controller.value * 2.0 * 3.1415926535,
              child: child,
            );
          },
        ),
      ),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }
}

class ExpensiveStaticCard extends StatelessWidget {
  const ExpensiveStaticCard({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 150,
      height: 150,
      decoration: const BoxDecoration(
        color: Color(0xFF2196F3),
        borderRadius: BorderRadius.all(Radius.circular(16)),
      ),
      child: const Center(
        child: Text(
          'Optimized Card',
          style: TextStyle(color: Color(0xFFFFFFFF)),
        ),
      ),
    );
  }
}
