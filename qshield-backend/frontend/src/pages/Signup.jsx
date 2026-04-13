import { useState, useContext } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

export default function Signup() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      const response = await fetch('http://localhost:8000/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Registration failed');
      }
      const loginResponse = await fetch('http://localhost:8000/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ username: email, password: password }),
      });
      const loginData = await loginResponse.json();
      login(loginData.access_token);
      navigate('/');
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="min-h-screen flex bg-[#fef8f3]">
      {/* Left branding panel */}
      <div className="hidden lg:flex flex-col justify-between w-80 bg-gradient-to-b from-[#81001d] to-[#a51c30] p-10 shadow-2xl">
        <div>
          <h1 className="text-xl font-bold text-white tracking-tighter uppercase">Luminous Guardian</h1>
          <p className="text-[10px] text-white/50 font-medium tracking-[0.2em] uppercase mt-1">Ethereal Fortress v1.0</p>
        </div>
        <div>
          <span className="material-symbols-outlined text-white/20 text-[120px] block mb-4" style={{ fontVariationSettings: "'FILL' 1" }}>security</span>
          <p className="text-white/60 text-sm leading-relaxed">Create your account to access the quantum-safe security command center.</p>
        </div>
        <p className="text-white/30 text-xs">© 2024 Luminous Guardian Security Services</p>
      </div>

      {/* Right signup form */}
      <div className="flex-1 flex items-center justify-center px-8">
        <div className="max-w-md w-full">
          <div className="mb-10">
            <h2 className="text-3xl font-bold text-[#81001d] tracking-tight">Create account</h2>
            <p className="text-[#594141] mt-2 text-sm">Join Requiem to start monitoring your assets</p>
          </div>

          {error && (
            <div className="bg-red-500/10 border border-red-400/40 text-red-700 p-3 rounded-xl mb-6 text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSignup} className="space-y-5">
            <div>
              <label className="block text-xs font-bold text-[#594141] uppercase tracking-widest mb-2">Email</label>
              <input
                type="email"
                required
                className="w-full bg-white border border-[#e1bebe] rounded-xl px-4 py-3 text-[#1d1b19] text-sm focus:outline-none focus:border-[#81001d] focus:ring-2 focus:ring-[#81001d]/20 transition-all placeholder:text-[#8d7070]"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="admin@requiem.com"
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-[#594141] uppercase tracking-widest mb-2">Password</label>
              <input
                type="password"
                required
                className="w-full bg-white border border-[#e1bebe] rounded-xl px-4 py-3 text-[#1d1b19] text-sm focus:outline-none focus:border-[#81001d] focus:ring-2 focus:ring-[#81001d]/20 transition-all placeholder:text-[#8d7070]"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
              />
            </div>

            <button
              type="submit"
              className="w-full bg-gradient-to-r from-[#81001d] to-[#a51c30] hover:from-[#6a0018] hover:to-[#8e1829] text-white font-bold py-3 rounded-xl uppercase text-xs tracking-widest shadow-lg shadow-[#81001d]/30 active:scale-95 transition-all"
            >
              Create Account
            </button>
          </form>

          <div className="mt-8 text-center text-sm text-[#594141]">
            Already have an account?{' '}
            <Link to="/login" className="text-[#964900] font-bold hover:text-[#81001d] transition-colors">
              Sign in
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
