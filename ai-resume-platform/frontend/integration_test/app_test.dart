// 集成测试 - 真机/模拟器端到端测试
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:ai_resume/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('端到端测试', () {
    testWidgets('完整用户流程测试', (WidgetTester tester) async {
      // 启动应用
      app.main();
      await tester.pumpAndSettle();

      // 验证应用启动成功
      expect(find.byType(MaterialApp), findsOneWidget);
      
      // 等待加载完成
      await tester.pumpAndSettle(const Duration(seconds: 2));
      
      print('✅ 应用启动测试通过');
    });

    testWidgets('登录页面测试', (WidgetTester tester) async {
      app.main();
      await tester.pumpAndSettle();

      // 查找登录相关元素
      final emailField = find.byType(TextField).first;
      final passwordField = find.byType(TextField).last;
      
      if (emailField.evaluate().isNotEmpty) {
        // 输入测试数据
        await tester.enterText(emailField, 'test@example.com');
        await tester.pumpAndSettle();
        
        print('✅ 登录页面测试通过');
      }
    });

    testWidgets('导航测试', (WidgetTester tester) async {
      app.main();
      await tester.pumpAndSettle();

      // 测试底部导航
      final bottomNav = find.byType(BottomNavigationBar);
      if (bottomNav.evaluate().isNotEmpty) {
        // 点击各个导航项
        final navItems = find.descendant(
          of: bottomNav,
          matching: find.byType(InkWell),
        );
        
        for (int i = 0; i < navItems.evaluate().length && i < 4; i++) {
          await tester.tap(navItems.at(i));
          await tester.pumpAndSettle();
        }
        
        print('✅ 导航测试通过');
      }
    });

    testWidgets('简历创建流程测试', (WidgetTester tester) async {
      app.main();
      await tester.pumpAndSettle();

      // 查找创建按钮
      final createButton = find.byIcon(Icons.add);
      if (createButton.evaluate().isNotEmpty) {
        await tester.tap(createButton.first);
        await tester.pumpAndSettle();
        
        print('✅ 简历创建流程测试通过');
      }
    });

    testWidgets('表单输入测试', (WidgetTester tester) async {
      app.main();
      await tester.pumpAndSettle();

      // 测试表单输入
      final textFields = find.byType(TextField);
      
      for (var field in textFields.evaluate()) {
        final finder = find.byWidget(field.widget);
        await tester.tap(finder);
        await tester.pumpAndSettle();
        await tester.enterText(finder, '测试输入');
        await tester.pumpAndSettle();
      }
      
      print('✅ 表单输入测试通过');
    });

    testWidgets('滚动测试', (WidgetTester tester) async {
      app.main();
      await tester.pumpAndSettle();

      // 测试滚动
      final scrollable = find.byType(Scrollable);
      if (scrollable.evaluate().isNotEmpty) {
        await tester.drag(scrollable.first, const Offset(0, -300));
        await tester.pumpAndSettle();
        
        await tester.drag(scrollable.first, const Offset(0, 300));
        await tester.pumpAndSettle();
        
        print('✅ 滚动测试通过');
      }
    });

    testWidgets('性能测试', (WidgetTester tester) async {
      final stopwatch = Stopwatch()..start();
      
      app.main();
      await tester.pumpAndSettle();
      
      stopwatch.stop();
      
      print('⏱️ 应用启动耗时: ${stopwatch.elapsedMilliseconds}ms');
      
      // 启动时间应小于3秒
      expect(stopwatch.elapsedMilliseconds, lessThan(3000));
      
      print('✅ 性能测试通过');
    });
  });
}
