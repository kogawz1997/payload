abstract class AuthService {
  Future<String> signInWithProvider(String provider);
  Future<void> signOut();
}
