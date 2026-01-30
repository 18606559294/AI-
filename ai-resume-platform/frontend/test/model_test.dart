// 数据模型单元测试
import 'package:flutter_test/flutter_test.dart';

// 简历模型测试
class Resume {
  final int id;
  final String title;
  final String? content;
  final DateTime createdAt;
  final DateTime updatedAt;

  Resume({
    required this.id,
    required this.title,
    this.content,
    required this.createdAt,
    required this.updatedAt,
  });

  factory Resume.fromJson(Map<String, dynamic> json) {
    return Resume(
      id: json['id'],
      title: json['title'],
      content: json['content'],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'content': content,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }
}

// 用户模型测试
class User {
  final int id;
  final String email;
  final String? phone;
  final String role;

  User({
    required this.id,
    required this.email,
    this.phone,
    this.role = 'user',
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      email: json['email'],
      phone: json['phone'],
      role: json['role'] ?? 'user',
    );
  }

  bool get isPremium => role == 'premium' || role == 'enterprise';
}

void main() {
  group('Resume Model Tests', () {
    test('Resume should be created from JSON', () {
      final json = {
        'id': 1,
        'title': '软件工程师简历',
        'content': '{"basic_info": {}}',
        'created_at': '2026-01-27T10:00:00Z',
        'updated_at': '2026-01-27T12:00:00Z',
      };

      final resume = Resume.fromJson(json);

      expect(resume.id, 1);
      expect(resume.title, '软件工程师简历');
      expect(resume.content, '{"basic_info": {}}');
    });

    test('Resume should convert to JSON', () {
      final resume = Resume(
        id: 1,
        title: '测试简历',
        content: null,
        createdAt: DateTime(2026, 1, 27, 10, 0),
        updatedAt: DateTime(2026, 1, 27, 12, 0),
      );

      final json = resume.toJson();

      expect(json['id'], 1);
      expect(json['title'], '测试简历');
      expect(json['content'], isNull);
    });

    test('Resume with empty title should still work', () {
      final resume = Resume(
        id: 1,
        title: '',
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      );

      expect(resume.title, '');
    });
  });

  group('User Model Tests', () {
    test('User should be created from JSON', () {
      final json = {
        'id': 1,
        'email': 'test@example.com',
        'phone': '13800138000',
        'role': 'premium',
      };

      final user = User.fromJson(json);

      expect(user.id, 1);
      expect(user.email, 'test@example.com');
      expect(user.phone, '13800138000');
      expect(user.role, 'premium');
    });

    test('User should have default role', () {
      final json = {
        'id': 1,
        'email': 'test@example.com',
      };

      final user = User.fromJson(json);
      expect(user.role, 'user');
    });

    test('Premium user check should work', () {
      final premiumUser = User(id: 1, email: 'a@b.com', role: 'premium');
      final normalUser = User(id: 2, email: 'b@c.com', role: 'user');

      expect(premiumUser.isPremium, isTrue);
      expect(normalUser.isPremium, isFalse);
    });
  });

  group('Validation Tests', () {
    test('Email validation', () {
      bool isValidEmail(String email) {
        return RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$').hasMatch(email);
      }

      expect(isValidEmail('test@example.com'), isTrue);
      expect(isValidEmail('invalid-email'), isFalse);
      expect(isValidEmail('test@'), isFalse);
      expect(isValidEmail('@example.com'), isFalse);
    });

    test('Phone validation', () {
      bool isValidPhone(String phone) {
        return RegExp(r'^1[3-9]\d{9}$').hasMatch(phone);
      }

      expect(isValidPhone('13800138000'), isTrue);
      expect(isValidPhone('12345678901'), isFalse);
      expect(isValidPhone('1380013800'), isFalse);
    });

    test('Password strength validation', () {
      int getPasswordStrength(String password) {
        int score = 0;
        if (password.length >= 8) score++;
        if (RegExp(r'[0-9]').hasMatch(password)) score++;
        if (RegExp(r'[a-z]').hasMatch(password)) score++;
        if (RegExp(r'[A-Z]').hasMatch(password)) score++;
        if (RegExp(r'[!@#$%^&*(),.?":{}|<>]').hasMatch(password)) score++;
        return score;
      }

      expect(getPasswordStrength('weak'), 1);  // 短密码只有小写字母
      expect(getPasswordStrength('Stronger1'), 4);
      expect(getPasswordStrength('VeryStr0ng!'), 5);
    });
  });
}
