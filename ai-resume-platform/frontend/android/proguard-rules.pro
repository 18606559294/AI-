# Add project specific ProGuard rules here.
# You can control the set of applied configuration files using the
# proguardFiles setting in build.gradle.

# Flutter specific rules
-keep class io.flutter.app.** { *; }
-keep class io.flutter.plugin.**  { *; }
-keep class io.flutter.util.**  { *; }
-keep class io.flutter.view.**  { *; }
-keep class io.flutter.**  { *; }
-keep class io.flutter.plugins.**  { *; }

# Keep models
-keep class com.example.ai_resume_app.models.** { *; }

# Keep providers
-keep class com.example.ai_resume_app.providers.** { *; }

# Keep Stetho
-keep class com.facebook.stetho.** { *; }
-keep class com.facebook.stetho.inspector.** { *; }

# Keep LeakCanary
-dontwarn leakcanary.**
-keep class leakcanary.** { *; }

# Keep OkHttp
-dontwarn okhttp3.**
-keep class okhttp3.** { *; }
-keep interface okhttp3.** { *; }

# Keep Retrofit
-dontwarn retrofit2.**
-keep class retrofit2.** { *; }
-keepattributes Signature
-keepattributes Exceptions

# Keep Gson
-keepattributes Signature
-keepattributes *Annotation*
-dontwarn sun.misc.**
-keep class com.google.gson.** { *; }
-keep class * implements com.google.gson.TypeAdapter
-keep class * implements com.google.gson.TypeAdapterFactory
-keep class * implements com.google.gson.JsonSerializer
-keep class * implements com.google.gson.JsonDeserializer

# Keep RxJava/RxKotlin
-dontwarn rx.**
-dontwarn io.reactivex.**
-keep class rx.** { *; }
-keep class io.reactivex.** { *; }

# Keep Room database
-keep class * extends androidx.room.RoomDatabase
-dontwarn androidx.room.paging.**

# Keep Kotlin coroutines
-keepnames class kotlinx.coroutines.internal.MainDispatcherFactory {}
-keepnames class kotlinx.coroutines.CoroutineExceptionHandler {}
-keepclassmembernames class kotlinx.** {
    volatile <fields>;
}

# Keep JSON annotations
-keepattributes *Annotation*
-keep class com.google.gson.annotations.** { *; }

# Optimize
-optimizationpasses 5
-dontusemixedcaseclassnames
-dontskipnonpubliclibraryclasses
-dontpreverify
-verbose

# Remove logging in release builds
-assumenosideeffects class android.util.Log {
    public static boolean isLoggable(java.lang.String, int);
    public static int v(...);
    public static int d(...);
    public static int i(...);
    public static int w(...);
    public static int e(...);
}

# Preserve native methods
-keepclasseswithmembernames class * {
    native <methods>;
}

# Keep enum classes
-keepclassmembers enum * {
    public static **[] values();
    public static ** valueOf(java.lang.String);
}

# Keep Parcelable
-keep class * implements android.os.Parcelable {
    public static final android.os.Parcelable$Creator *;
}

# Keep Serializable
-keepclassmembers class * implements java.io.Serializable {
    static final long serialVersionUID;
    private static final java.io.ObjectStreamField[] serialPersistentFields;
    private void writeObject(java.io.ObjectOutputStream);
    private void readObject(java.io.ObjectInputStream);
    java.lang.Object writeReplace();
    java.lang.Object readResolve();
}

# Keep View constructors
-keepclasseswithmembers class * extends android.view.View {
    <init>(android.content.Context);
    <init>(android.content.Context, android.util.AttributeSet);
    <init>(android.content.Context, android.util.AttributeSet, int);
}

# Keep Activity/Fragment constructors
-keepclassmembers class * extends android.app.Activity {
    public <init>();
}

-keepclassmembers class * extends androidx.fragment.app.Fragment {
    public <init>();
}

# Keep custom views
-keepclassmembers class * extends android.view.View {
    public <init>(android.content.Context);
    public <init>(android.content.Context, android.util.AttributeSet);
    public <init>(android.content.Context, android.util.AttributeSet, int);
    public void set*(...);
}

# Prevent obfuscation of classes with specific annotations
-keep @androidx.annotation.Keep class * {*;}
-keep @androidx.annotation.Keep class * { public <init>(); }
-keep @androidx.annotation.Keep class * { public <methods>; }
-keep @androidx.annotation.Keep class * { public <fields>; }
-keep @androidx.annotation.Keep class * { *; }

# Keep data classes
-keep @androidx.annotation.Keep class * extends java.lang.Exception { *; }

# Keep methods with specific annotations
-keepclassmembers class * {
    @androidx.annotation.Keep <methods>;
}

-keepclassmembers class * {
    @androidx.annotation.Keep <fields>;
}