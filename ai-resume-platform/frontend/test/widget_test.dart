// Widget 组件测试
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('Custom Button Widget Tests', () {
    testWidgets('Button should display correct text', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: ElevatedButton(
              onPressed: () {},
              child: const Text('测试按钮'),
            ),
          ),
        ),
      );
      
      expect(find.text('测试按钮'), findsOneWidget);
      expect(find.byType(ElevatedButton), findsOneWidget);
    });

    testWidgets('Button should respond to tap', (WidgetTester tester) async {
      bool tapped = false;
      
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: ElevatedButton(
              onPressed: () => tapped = true,
              child: const Text('点击测试'),
            ),
          ),
        ),
      );
      
      await tester.tap(find.byType(ElevatedButton));
      expect(tapped, isTrue);
    });
  });

  group('Form Widget Tests', () {
    testWidgets('TextField should accept input', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: TextField(
              decoration: const InputDecoration(
                labelText: '邮箱',
                hintText: '请输入邮箱',
              ),
            ),
          ),
        ),
      );
      
      await tester.enterText(find.byType(TextField), 'test@example.com');
      expect(find.text('test@example.com'), findsOneWidget);
    });

    testWidgets('Form validation should work', (WidgetTester tester) async {
      final formKey = GlobalKey<FormState>();
      String? emailError;
      
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: Form(
              key: formKey,
              child: TextFormField(
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return '邮箱不能为空';
                  }
                  if (!value.contains('@')) {
                    return '邮箱格式不正确';
                  }
                  return null;
                },
                onSaved: (value) {},
              ),
            ),
          ),
        ),
      );
      
      // 验证空值
      formKey.currentState!.validate();
      await tester.pump();
      expect(find.text('邮箱不能为空'), findsOneWidget);
    });
  });

  group('Card Widget Tests', () {
    testWidgets('Card should display content correctly', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: Card(
              child: ListTile(
                leading: const Icon(Icons.description),
                title: const Text('我的简历'),
                subtitle: const Text('最后编辑: 2026-01-27'),
              ),
            ),
          ),
        ),
      );
      
      expect(find.text('我的简历'), findsOneWidget);
      expect(find.text('最后编辑: 2026-01-27'), findsOneWidget);
      expect(find.byIcon(Icons.description), findsOneWidget);
    });
  });

  group('ListView Tests', () {
    testWidgets('ListView should render items', (WidgetTester tester) async {
      final items = ['简历1', '简历2', '简历3'];
      
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: ListView.builder(
              itemCount: items.length,
              itemBuilder: (context, index) {
                return ListTile(
                  title: Text(items[index]),
                );
              },
            ),
          ),
        ),
      );
      
      for (var item in items) {
        expect(find.text(item), findsOneWidget);
      }
    });
  });
}
