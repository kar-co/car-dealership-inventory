import { useEffect, useMemo, useState } from "react";

import { request } from "./api";

const blankVehicle = { make: "", model: "", category: "", price: "", quantity: "" };

function sessionFromToken(token, email) {
  const encoded = token.split(".")[1].replace(/-/g, "+").replace(/_/g, "/");
  return { token, email: email.toLowerCase(), isAdmin: JSON.parse(atob(encoded)).is_admin === true };
}

function Authentication({ mode, setMode, authenticate }) {
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const login = mode === "login";

  async function submit(event) {
    event.preventDefault();
    setError("");
    setLoading(true);
    try {
      if (!login) await request("/auth/register", { method: "POST", body: JSON.stringify(form) });
      const result = await request("/auth/login", { method: "POST", body: JSON.stringify(form) });
      authenticate(sessionFromToken(result.access_token, form.email));
    } catch (requestError) { setError(requestError.message); }
    finally { setLoading(false); }
  }

  return <main className="grid min-h-screen place-items-center p-5"><section className="grid w-full max-w-4xl overflow-hidden rounded-3xl bg-white shadow-card md:grid-cols-2"><aside className="hidden bg-indigo-700 p-10 text-white md:block"><p className="text-sm font-semibold uppercase tracking-[.2em] text-indigo-200">Northstar Motors</p><h1 className="mt-8 text-4xl font-semibold">Inventory, made clear.</h1><p className="mt-5 text-indigo-100">Browse vehicles, refine your search, and manage stock in one focused workspace.</p></aside><section className="p-7 sm:p-10"><p className="text-sm font-medium text-indigo-600">{login ? "Welcome back" : "Create your account"}</p><h1 className="mt-2 text-3xl font-semibold text-slate-900">{login ? "Sign in" : "Register"}</h1><form className="mt-8 space-y-5" onSubmit={submit}><label className="block text-sm font-medium">Email<input className="mt-2 w-full rounded-xl border border-slate-300 px-4 py-3" type="email" value={form.email} onChange={(event) => setForm({ ...form, email: event.target.value })} required /></label><label className="block text-sm font-medium">Password<input className="mt-2 w-full rounded-xl border border-slate-300 px-4 py-3" type="password" minLength="8" value={form.password} onChange={(event) => setForm({ ...form, password: event.target.value })} required /></label>{error && <p className="rounded-xl bg-red-50 p-3 text-sm text-red-700" role="alert">{error}</p>}<button className="w-full rounded-xl bg-indigo-600 px-4 py-3 font-semibold text-white disabled:opacity-60" disabled={loading}>{loading ? "Please wait..." : login ? "Sign in" : "Create account"}</button></form><button className="mt-6 text-sm font-medium text-indigo-700" onClick={() => setMode(login ? "register" : "login")}>{login ? "Need an account? Register" : "Already have an account? Sign in"}</button></section></section></main>;
}

function VehicleEditor({ initial = blankVehicle, label, onSave, onCancel }) {
  const [vehicle, setVehicle] = useState(initial);
  const [saving, setSaving] = useState(false);
  useEffect(() => setVehicle(initial), [initial]);
  async function submit(event) { event.preventDefault(); setSaving(true); try { await onSave({ ...vehicle, price: Number(vehicle.price), quantity: Number(vehicle.quantity) }); } finally { setSaving(false); } }
  return <form className="grid gap-3 sm:grid-cols-2" onSubmit={submit}>{Object.entries(vehicle).map(([name, value]) => <label className="text-sm font-medium" key={name}>{name[0].toUpperCase() + name.slice(1)}<input className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2" type={name === "price" || name === "quantity" ? "number" : "text"} min={name === "price" ? "0.01" : name === "quantity" ? "0" : undefined} step={name === "price" ? "0.01" : "1"} value={value} onChange={(event) => setVehicle({ ...vehicle, [name]: event.target.value })} required /></label>)}<div className="flex gap-3 sm:col-span-2"><button className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white disabled:opacity-60" disabled={saving}>{saving ? "Saving..." : label}</button>{onCancel && <button className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-semibold" type="button" onClick={onCancel}>Cancel</button>}</div></form>;
}

function Dashboard({ session, logout }) {
  const [vehicles, setVehicles] = useState([]); const [query, setQuery] = useState(""); const [category, setCategory] = useState("all"); const [minPrice, setMinPrice] = useState(""); const [maxPrice, setMaxPrice] = useState(""); const [loading, setLoading] = useState(true); const [error, setError] = useState(""); const [adding, setAdding] = useState(false); const [editing, setEditing] = useState(null);
  const categories = useMemo(() => [...new Set(vehicles.map(({ category: value }) => value))], [vehicles]);
  const visible = vehicles.filter((vehicle) => category === "all" || vehicle.category === category);
  async function load() { const params = new URLSearchParams(); if (query) params.set("query", query); if (minPrice) params.set("min_price", minPrice); if (maxPrice) params.set("max_price", maxPrice); setLoading(true); setError(""); try { setVehicles(await request(params.size ? `/vehicles/search?${params}` : "/vehicles", { token: session.token })); } catch (requestError) { setError(requestError.message); } finally { setLoading(false); } }
  useEffect(() => { load(); }, []);
  async function purchase(vehicle) { try { await request(`/vehicles/${vehicle.id}/purchase`, { method: "POST", token: session.token, body: JSON.stringify({ quantity: 1 }) }); await load(); } catch (requestError) { setError(requestError.message); } }
  async function save(payload) { try { await request(editing ? `/vehicles/${editing.id}` : "/vehicles", { method: editing ? "PUT" : "POST", token: session.token, body: JSON.stringify(payload) }); setAdding(false); setEditing(null); await load(); } catch (requestError) { setError(requestError.message); } }
  async function remove(id) { if (!window.confirm("Delete this vehicle?")) return; try { await request(`/vehicles/${id}`, { method: "DELETE", token: session.token }); await load(); } catch (requestError) { setError(requestError.message); } }
  return <main className="min-h-screen"><header className="border-b bg-white"><div className="mx-auto flex max-w-7xl items-center justify-between p-5"><div><p className="text-xs font-bold uppercase tracking-[.18em] text-indigo-600">Northstar Motors</p><h1 className="text-xl font-semibold">Vehicle inventory</h1></div><div className="flex items-center gap-3"><span className="hidden text-sm text-slate-500 sm:inline">{session.email}</span><button className="rounded-lg border px-3 py-2 text-sm font-semibold" onClick={logout}>Sign out</button></div></div></header><section className="mx-auto max-w-7xl p-5 sm:p-8"><div className="mb-6 flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between"><div><p className="text-sm font-medium text-indigo-600">Current stock</p><h2 className="text-3xl font-semibold">Find the right vehicle</h2></div>{session.isAdmin && <button className="rounded-xl bg-indigo-600 px-4 py-3 font-semibold text-white" onClick={() => { setEditing(null); setAdding(true); }}>Add vehicle</button>}</div><div className="mb-6 grid gap-3 rounded-2xl bg-white p-4 shadow-card sm:grid-cols-2 lg:grid-cols-[1fr_180px_150px_150px_auto]"><input className="rounded-xl border px-4 py-3" placeholder="Search make, model, or category" value={query} onChange={(event) => setQuery(event.target.value)} /><select className="rounded-xl border px-4 py-3" value={category} onChange={(event) => setCategory(event.target.value)}><option value="all">All categories</option>{categories.map((value) => <option key={value}>{value}</option>)}</select><input className="rounded-xl border px-4 py-3" placeholder="Min price" type="number" min="0" value={minPrice} onChange={(event) => setMinPrice(event.target.value)} /><input className="rounded-xl border px-4 py-3" placeholder="Max price" type="number" min="0" value={maxPrice} onChange={(event) => setMaxPrice(event.target.value)} /><button className="rounded-xl bg-slate-900 px-5 py-3 font-semibold text-white" onClick={load}>Search</button></div>{error && <p className="mb-5 rounded-xl bg-red-50 p-4 text-sm text-red-700" role="alert">{error}</p>}{adding && <section className="mb-6 rounded-2xl bg-white p-5 shadow-card"><h3 className="mb-4 text-lg font-semibold">Add vehicle</h3><VehicleEditor label="Add vehicle" onSave={save} onCancel={() => setAdding(false)} /></section>}{loading ? <p className="py-12 text-center text-slate-500">Loading vehicles...</p> : visible.length === 0 ? <p className="py-12 text-center text-slate-500">No vehicles match your search.</p> : <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">{visible.map((vehicle) => <article className="rounded-2xl bg-white p-5 shadow-card" key={vehicle.id}>{editing?.id === vehicle.id ? <><h3 className="mb-4 text-lg font-semibold">Update vehicle</h3><VehicleEditor initial={{ ...vehicle, price: String(vehicle.price), quantity: String(vehicle.quantity) }} label="Save changes" onSave={save} onCancel={() => setEditing(null)} /></> : <><div className="flex items-start justify-between gap-3"><div><p className="text-sm font-medium text-indigo-600">{vehicle.category}</p><h3 className="mt-1 text-xl font-semibold">{vehicle.make} {vehicle.model}</h3></div><span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-bold">{vehicle.quantity} in stock</span></div><p className="mt-5 text-2xl font-semibold">${Number(vehicle.price).toLocaleString(undefined, { minimumFractionDigits: 2 })}</p><div className="mt-5 flex flex-wrap gap-2"><button className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white disabled:bg-slate-300" disabled={!vehicle.quantity} onClick={() => purchase(vehicle)}>{vehicle.quantity ? "Purchase" : "Sold out"}</button>{session.isAdmin && <><button className="rounded-lg border px-4 py-2 text-sm font-semibold" onClick={() => setEditing(vehicle)}>Update</button><button className="rounded-lg border border-red-200 px-4 py-2 text-sm font-semibold text-red-700" onClick={() => remove(vehicle.id)}>Delete</button></>}</div></>}</article>)}</div>}</section></main>;
}

export default function App() {
  const [session, setSession] = useState(() => JSON.parse(localStorage.getItem("dealership-session") || "null")); const [mode, setMode] = useState("login");
  function authenticate(value) { localStorage.setItem("dealership-session", JSON.stringify(value)); setSession(value); }
  function logout() { localStorage.removeItem("dealership-session"); setSession(null); }
  return session ? <Dashboard session={session} logout={logout} /> : <Authentication mode={mode} setMode={setMode} authenticate={authenticate} />;
}
