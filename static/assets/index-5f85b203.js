(function () {
  const t = document.createElement("link").relList;
  if (t && t.supports && t.supports("modulepreload")) return;
  for (const s of document.querySelectorAll('link[rel="modulepreload"]')) o(s);
  new MutationObserver((s) => {
    for (const r of s)
      if (r.type === "childList")
        for (const i of r.addedNodes)
          i.tagName === "LINK" && i.rel === "modulepreload" && o(i);
  }).observe(document, { childList: !0, subtree: !0 });
  function n(s) {
    const r = {};
    return (
      s.integrity && (r.integrity = s.integrity),
      s.referrerPolicy && (r.referrerPolicy = s.referrerPolicy),
      s.crossOrigin === "use-credentials"
        ? (r.credentials = "include")
        : s.crossOrigin === "anonymous"
        ? (r.credentials = "omit")
        : (r.credentials = "same-origin"),
      r
    );
  }
  function o(s) {
    if (s.ep) return;
    s.ep = !0;
    const r = n(s);
    fetch(s.href, r);
  }
})();
function Ps(e, t) {
  const n = Object.create(null),
    o = e.split(",");
  for (let s = 0; s < o.length; s++) n[o[s]] = !0;
  return t ? (s) => !!n[s.toLowerCase()] : (s) => !!n[s];
}
const pe = {},
  Qt = [],
  qe = () => {},
  Fa = () => !1,
  Da = /^on[^a-z]/,
  go = (e) => Da.test(e),
  Rs = (e) => e.startsWith("onUpdate:"),
  be = Object.assign,
  As = (e, t) => {
    const n = e.indexOf(t);
    n > -1 && e.splice(n, 1);
  },
  Ua = Object.prototype.hasOwnProperty,
  ie = (e, t) => Ua.call(e, t),
  W = Array.isArray,
  en = (e) => _o(e) === "[object Map]",
  Ji = (e) => _o(e) === "[object Set]",
  Y = (e) => typeof e == "function",
  we = (e) => typeof e == "string",
  js = (e) => typeof e == "symbol",
  me = (e) => e !== null && typeof e == "object",
  Gi = (e) => me(e) && Y(e.then) && Y(e.catch),
  Yi = Object.prototype.toString,
  _o = (e) => Yi.call(e),
  za = (e) => _o(e).slice(8, -1),
  Qi = (e) => _o(e) === "[object Object]",
  $s = (e) =>
    we(e) && e !== "NaN" && e[0] !== "-" && "" + parseInt(e, 10) === e,
  Gn = Ps(
    ",key,ref,ref_for,ref_key,onVnodeBeforeMount,onVnodeMounted,onVnodeBeforeUpdate,onVnodeUpdated,onVnodeBeforeUnmount,onVnodeUnmounted"
  ),
  yo = (e) => {
    const t = Object.create(null);
    return (n) => t[n] || (t[n] = e(n));
  },
  Ka = /-(\w)/g,
  ot = yo((e) => e.replace(Ka, (t, n) => (n ? n.toUpperCase() : ""))),
  Ha = /\B([A-Z])/g,
  Bt = yo((e) => e.replace(Ha, "-$1").toLowerCase()),
  vo = yo((e) => e.charAt(0).toUpperCase() + e.slice(1)),
  No = yo((e) => (e ? `on${vo(e)}` : "")),
  Tn = (e, t) => !Object.is(e, t),
  Yn = (e, t) => {
    for (let n = 0; n < e.length; n++) e[n](t);
  },
  io = (e, t, n) => {
    Object.defineProperty(e, t, { configurable: !0, enumerable: !1, value: n });
  },
  ns = (e) => {
    const t = parseFloat(e);
    return isNaN(t) ? e : t;
  },
  Ba = (e) => {
    const t = we(e) ? Number(e) : NaN;
    return isNaN(t) ? e : t;
  };
let vr;
const os = () =>
  vr ||
  (vr =
    typeof globalThis < "u"
      ? globalThis
      : typeof self < "u"
      ? self
      : typeof window < "u"
      ? window
      : typeof global < "u"
      ? global
      : {});
function bo(e) {
  if (W(e)) {
    const t = {};
    for (let n = 0; n < e.length; n++) {
      const o = e[n],
        s = we(o) ? qa(o) : bo(o);
      if (s) for (const r in s) t[r] = s[r];
    }
    return t;
  } else {
    if (we(e)) return e;
    if (me(e)) return e;
  }
}
const Wa = /;(?![^(]*\))/g,
  Va = /:([^]+)/,
  Za = new RegExp("\\/\\*.*?\\*\\/", "gs");
function qa(e) {
  const t = {};
  return (
    e
      .replace(Za, "")
      .split(Wa)
      .forEach((n) => {
        if (n) {
          const o = n.split(Va);
          o.length > 1 && (t[o[0].trim()] = o[1].trim());
        }
      }),
    t
  );
}
function Kt(e) {
  let t = "";
  if (we(e)) t = e;
  else if (W(e))
    for (let n = 0; n < e.length; n++) {
      const o = Kt(e[n]);
      o && (t += o + " ");
    }
  else if (me(e)) for (const n in e) e[n] && (t += n + " ");
  return t.trim();
}
const Xa =
    "itemscope,allowfullscreen,formnovalidate,ismap,nomodule,novalidate,readonly",
  Ja = Ps(Xa);
function ec(e) {
  return !!e || e === "";
}
const Ce = (e) =>
    we(e)
      ? e
      : e == null
      ? ""
      : W(e) || (me(e) && (e.toString === Yi || !Y(e.toString)))
      ? JSON.stringify(e, tc, 2)
      : String(e),
  tc = (e, t) =>
    t && t.__v_isRef
      ? tc(e, t.value)
      : en(t)
      ? {
          [`Map(${t.size})`]: [...t.entries()].reduce(
            (n, [o, s]) => ((n[`${o} =>`] = s), n),
            {}
          ),
        }
      : Ji(t)
      ? { [`Set(${t.size})`]: [...t.values()] }
      : me(t) && !W(t) && !Qi(t)
      ? String(t)
      : t;
let De;
class nc {
  constructor(t = !1) {
    (this.detached = t),
      (this._active = !0),
      (this.effects = []),
      (this.cleanups = []),
      (this.parent = De),
      !t && De && (this.index = (De.scopes || (De.scopes = [])).push(this) - 1);
  }
  get active() {
    return this._active;
  }
  run(t) {
    if (this._active) {
      const n = De;
      try {
        return (De = this), t();
      } finally {
        De = n;
      }
    }
  }
  on() {
    De = this;
  }
  off() {
    De = this.parent;
  }
  stop(t) {
    if (this._active) {
      let n, o;
      for (n = 0, o = this.effects.length; n < o; n++) this.effects[n].stop();
      for (n = 0, o = this.cleanups.length; n < o; n++) this.cleanups[n]();
      if (this.scopes)
        for (n = 0, o = this.scopes.length; n < o; n++) this.scopes[n].stop(!0);
      if (!this.detached && this.parent && !t) {
        const s = this.parent.scopes.pop();
        s &&
          s !== this &&
          ((this.parent.scopes[this.index] = s), (s.index = this.index));
      }
      (this.parent = void 0), (this._active = !1);
    }
  }
}
function oc(e) {
  return new nc(e);
}
function Ga(e, t = De) {
  t && t.active && t.effects.push(e);
}
function Ls() {
  return De;
}
function sc(e) {
  De && De.cleanups.push(e);
}
const Ns = (e) => {
    const t = new Set(e);
    return (t.w = 0), (t.n = 0), t;
  },
  rc = (e) => (e.w & Ct) > 0,
  ic = (e) => (e.n & Ct) > 0,
  Ya = ({ deps: e }) => {
    if (e.length) for (let t = 0; t < e.length; t++) e[t].w |= Ct;
  },
  Qa = (e) => {
    const { deps: t } = e;
    if (t.length) {
      let n = 0;
      for (let o = 0; o < t.length; o++) {
        const s = t[o];
        rc(s) && !ic(s) ? s.delete(e) : (t[n++] = s),
          (s.w &= ~Ct),
          (s.n &= ~Ct);
      }
      t.length = n;
    }
  },
  co = new WeakMap();
let _n = 0,
  Ct = 1;
const ss = 30;
let We;
const Ut = Symbol(""),
  rs = Symbol("");
class Ms {
  constructor(t, n = null, o) {
    (this.fn = t),
      (this.scheduler = n),
      (this.active = !0),
      (this.deps = []),
      (this.parent = void 0),
      Ga(this, o);
  }
  run() {
    if (!this.active) return this.fn();
    let t = We,
      n = wt;
    for (; t; ) {
      if (t === this) return;
      t = t.parent;
    }
    try {
      return (
        (this.parent = We),
        (We = this),
        (wt = !0),
        (Ct = 1 << ++_n),
        _n <= ss ? Ya(this) : br(this),
        this.fn()
      );
    } finally {
      _n <= ss && Qa(this),
        (Ct = 1 << --_n),
        (We = this.parent),
        (wt = n),
        (this.parent = void 0),
        this.deferStop && this.stop();
    }
  }
  stop() {
    We === this
      ? (this.deferStop = !0)
      : this.active &&
        (br(this), this.onStop && this.onStop(), (this.active = !1));
  }
}
function br(e) {
  const { deps: t } = e;
  if (t.length) {
    for (let n = 0; n < t.length; n++) t[n].delete(e);
    t.length = 0;
  }
}
let wt = !0;
const cc = [];
function an() {
  cc.push(wt), (wt = !1);
}
function ln() {
  const e = cc.pop();
  wt = e === void 0 ? !0 : e;
}
function Me(e, t, n) {
  if (wt && We) {
    let o = co.get(e);
    o || co.set(e, (o = new Map()));
    let s = o.get(n);
    s || o.set(n, (s = Ns())), ac(s);
  }
}
function ac(e, t) {
  let n = !1;
  _n <= ss ? ic(e) || ((e.n |= Ct), (n = !rc(e))) : (n = !e.has(We)),
    n && (e.add(We), We.deps.push(e));
}
function ft(e, t, n, o, s, r) {
  const i = co.get(e);
  if (!i) return;
  let c = [];
  if (t === "clear") c = [...i.values()];
  else if (n === "length" && W(e)) {
    const a = Number(o);
    i.forEach((l, u) => {
      (u === "length" || u >= a) && c.push(l);
    });
  } else
    switch ((n !== void 0 && c.push(i.get(n)), t)) {
      case "add":
        W(e)
          ? $s(n) && c.push(i.get("length"))
          : (c.push(i.get(Ut)), en(e) && c.push(i.get(rs)));
        break;
      case "delete":
        W(e) || (c.push(i.get(Ut)), en(e) && c.push(i.get(rs)));
        break;
      case "set":
        en(e) && c.push(i.get(Ut));
        break;
    }
  if (c.length === 1) c[0] && is(c[0]);
  else {
    const a = [];
    for (const l of c) l && a.push(...l);
    is(Ns(a));
  }
}
function is(e, t) {
  const n = W(e) ? e : [...e];
  for (const o of n) o.computed && wr(o);
  for (const o of n) o.computed || wr(o);
}
function wr(e, t) {
  (e !== We || e.allowRecurse) && (e.scheduler ? e.scheduler() : e.run());
}
function el(e, t) {
  var n;
  return (n = co.get(e)) == null ? void 0 : n.get(t);
}
const tl = Ps("__proto__,__v_isRef,__isVue"),
  lc = new Set(
    Object.getOwnPropertyNames(Symbol)
      .filter((e) => e !== "arguments" && e !== "caller")
      .map((e) => Symbol[e])
      .filter(js)
  ),
  nl = Fs(),
  ol = Fs(!1, !0),
  sl = Fs(!0),
  xr = rl();
function rl() {
  const e = {};
  return (
    ["includes", "indexOf", "lastIndexOf"].forEach((t) => {
      e[t] = function (...n) {
        const o = re(this);
        for (let r = 0, i = this.length; r < i; r++) Me(o, "get", r + "");
        const s = o[t](...n);
        return s === -1 || s === !1 ? o[t](...n.map(re)) : s;
      };
    }),
    ["push", "pop", "shift", "unshift", "splice"].forEach((t) => {
      e[t] = function (...n) {
        an();
        const o = re(this)[t].apply(this, n);
        return ln(), o;
      };
    }),
    e
  );
}
function il(e) {
  const t = re(this);
  return Me(t, "has", e), t.hasOwnProperty(e);
}
function Fs(e = !1, t = !1) {
  return function (o, s, r) {
    if (s === "__v_isReactive") return !e;
    if (s === "__v_isReadonly") return e;
    if (s === "__v_isShallow") return t;
    if (s === "__v_raw" && r === (e ? (t ? xl : pc) : t ? hc : dc).get(o))
      return o;
    const i = W(o);
    if (!e) {
      if (i && ie(xr, s)) return Reflect.get(xr, s, r);
      if (s === "hasOwnProperty") return il;
    }
    const c = Reflect.get(o, s, r);
    return (js(s) ? lc.has(s) : tl(s)) || (e || Me(o, "get", s), t)
      ? c
      : ge(c)
      ? i && $s(s)
        ? c
        : c.value
      : me(c)
      ? e
        ? lt(c)
        : st(c)
      : c;
  };
}
const cl = uc(),
  al = uc(!0);
function uc(e = !1) {
  return function (n, o, s, r) {
    let i = n[o];
    if (nn(i) && ge(i) && !ge(s)) return !1;
    if (
      !e &&
      (!ao(s) && !nn(s) && ((i = re(i)), (s = re(s))), !W(n) && ge(i) && !ge(s))
    )
      return (i.value = s), !0;
    const c = W(n) && $s(o) ? Number(o) < n.length : ie(n, o),
      a = Reflect.set(n, o, s, r);
    return (
      n === re(r) && (c ? Tn(s, i) && ft(n, "set", o, s) : ft(n, "add", o, s)),
      a
    );
  };
}
function ll(e, t) {
  const n = ie(e, t);
  e[t];
  const o = Reflect.deleteProperty(e, t);
  return o && n && ft(e, "delete", t, void 0), o;
}
function ul(e, t) {
  const n = Reflect.has(e, t);
  return (!js(t) || !lc.has(t)) && Me(e, "has", t), n;
}
function fl(e) {
  return Me(e, "iterate", W(e) ? "length" : Ut), Reflect.ownKeys(e);
}
const fc = { get: nl, set: cl, deleteProperty: ll, has: ul, ownKeys: fl },
  dl = {
    get: sl,
    set(e, t) {
      return !0;
    },
    deleteProperty(e, t) {
      return !0;
    },
  },
  hl = be({}, fc, { get: ol, set: al }),
  Ds = (e) => e,
  wo = (e) => Reflect.getPrototypeOf(e);
function Hn(e, t, n = !1, o = !1) {
  e = e.__v_raw;
  const s = re(e),
    r = re(t);
  n || (t !== r && Me(s, "get", t), Me(s, "get", r));
  const { has: i } = wo(s),
    c = o ? Ds : n ? Ks : Pn;
  if (i.call(s, t)) return c(e.get(t));
  if (i.call(s, r)) return c(e.get(r));
  e !== s && e.get(t);
}
function Bn(e, t = !1) {
  const n = this.__v_raw,
    o = re(n),
    s = re(e);
  return (
    t || (e !== s && Me(o, "has", e), Me(o, "has", s)),
    e === s ? n.has(e) : n.has(e) || n.has(s)
  );
}
function Wn(e, t = !1) {
  return (
    (e = e.__v_raw), !t && Me(re(e), "iterate", Ut), Reflect.get(e, "size", e)
  );
}
function kr(e) {
  e = re(e);
  const t = re(this);
  return wo(t).has.call(t, e) || (t.add(e), ft(t, "add", e, e)), this;
}
function Cr(e, t) {
  t = re(t);
  const n = re(this),
    { has: o, get: s } = wo(n);
  let r = o.call(n, e);
  r || ((e = re(e)), (r = o.call(n, e)));
  const i = s.call(n, e);
  return (
    n.set(e, t), r ? Tn(t, i) && ft(n, "set", e, t) : ft(n, "add", e, t), this
  );
}
function Ir(e) {
  const t = re(this),
    { has: n, get: o } = wo(t);
  let s = n.call(t, e);
  s || ((e = re(e)), (s = n.call(t, e))), o && o.call(t, e);
  const r = t.delete(e);
  return s && ft(t, "delete", e, void 0), r;
}
function Sr() {
  const e = re(this),
    t = e.size !== 0,
    n = e.clear();
  return t && ft(e, "clear", void 0, void 0), n;
}
function Vn(e, t) {
  return function (o, s) {
    const r = this,
      i = r.__v_raw,
      c = re(i),
      a = t ? Ds : e ? Ks : Pn;
    return (
      !e && Me(c, "iterate", Ut), i.forEach((l, u) => o.call(s, a(l), a(u), r))
    );
  };
}
function Zn(e, t, n) {
  return function (...o) {
    const s = this.__v_raw,
      r = re(s),
      i = en(r),
      c = e === "entries" || (e === Symbol.iterator && i),
      a = e === "keys" && i,
      l = s[e](...o),
      u = n ? Ds : t ? Ks : Pn;
    return (
      !t && Me(r, "iterate", a ? rs : Ut),
      {
        next() {
          const { value: f, done: d } = l.next();
          return d
            ? { value: f, done: d }
            : { value: c ? [u(f[0]), u(f[1])] : u(f), done: d };
        },
        [Symbol.iterator]() {
          return this;
        },
      }
    );
  };
}
function pt(e) {
  return function (...t) {
    return e === "delete" ? !1 : this;
  };
}
function pl() {
  const e = {
      get(r) {
        return Hn(this, r);
      },
      get size() {
        return Wn(this);
      },
      has: Bn,
      add: kr,
      set: Cr,
      delete: Ir,
      clear: Sr,
      forEach: Vn(!1, !1),
    },
    t = {
      get(r) {
        return Hn(this, r, !1, !0);
      },
      get size() {
        return Wn(this);
      },
      has: Bn,
      add: kr,
      set: Cr,
      delete: Ir,
      clear: Sr,
      forEach: Vn(!1, !0),
    },
    n = {
      get(r) {
        return Hn(this, r, !0);
      },
      get size() {
        return Wn(this, !0);
      },
      has(r) {
        return Bn.call(this, r, !0);
      },
      add: pt("add"),
      set: pt("set"),
      delete: pt("delete"),
      clear: pt("clear"),
      forEach: Vn(!0, !1),
    },
    o = {
      get(r) {
        return Hn(this, r, !0, !0);
      },
      get size() {
        return Wn(this, !0);
      },
      has(r) {
        return Bn.call(this, r, !0);
      },
      add: pt("add"),
      set: pt("set"),
      delete: pt("delete"),
      clear: pt("clear"),
      forEach: Vn(!0, !0),
    };
  return (
    ["keys", "values", "entries", Symbol.iterator].forEach((r) => {
      (e[r] = Zn(r, !1, !1)),
        (n[r] = Zn(r, !0, !1)),
        (t[r] = Zn(r, !1, !0)),
        (o[r] = Zn(r, !0, !0));
    }),
    [e, n, t, o]
  );
}
const [ml, gl, _l, yl] = pl();
function Us(e, t) {
  const n = t ? (e ? yl : _l) : e ? gl : ml;
  return (o, s, r) =>
    s === "__v_isReactive"
      ? !e
      : s === "__v_isReadonly"
      ? e
      : s === "__v_raw"
      ? o
      : Reflect.get(ie(n, s) && s in o ? n : o, s, r);
}
const vl = { get: Us(!1, !1) },
  bl = { get: Us(!1, !0) },
  wl = { get: Us(!0, !1) },
  dc = new WeakMap(),
  hc = new WeakMap(),
  pc = new WeakMap(),
  xl = new WeakMap();
function kl(e) {
  switch (e) {
    case "Object":
    case "Array":
      return 1;
    case "Map":
    case "Set":
    case "WeakMap":
    case "WeakSet":
      return 2;
    default:
      return 0;
  }
}
function Cl(e) {
  return e.__v_skip || !Object.isExtensible(e) ? 0 : kl(za(e));
}
function st(e) {
  return nn(e) ? e : zs(e, !1, fc, vl, dc);
}
function Il(e) {
  return zs(e, !1, hl, bl, hc);
}
function lt(e) {
  return zs(e, !0, dl, wl, pc);
}
function zs(e, t, n, o, s) {
  if (!me(e) || (e.__v_raw && !(t && e.__v_isReactive))) return e;
  const r = s.get(e);
  if (r) return r;
  const i = Cl(e);
  if (i === 0) return e;
  const c = new Proxy(e, i === 2 ? o : n);
  return s.set(e, c), c;
}
function xt(e) {
  return nn(e) ? xt(e.__v_raw) : !!(e && e.__v_isReactive);
}
function nn(e) {
  return !!(e && e.__v_isReadonly);
}
function ao(e) {
  return !!(e && e.__v_isShallow);
}
function mc(e) {
  return xt(e) || nn(e);
}
function re(e) {
  const t = e && e.__v_raw;
  return t ? re(t) : e;
}
function on(e) {
  return io(e, "__v_skip", !0), e;
}
const Pn = (e) => (me(e) ? st(e) : e),
  Ks = (e) => (me(e) ? lt(e) : e);
function gc(e) {
  wt && We && ((e = re(e)), ac(e.dep || (e.dep = Ns())));
}
function _c(e, t) {
  e = re(e);
  const n = e.dep;
  n && is(n);
}
function ge(e) {
  return !!(e && e.__v_isRef === !0);
}
function se(e) {
  return yc(e, !1);
}
function Qn(e) {
  return yc(e, !0);
}
function yc(e, t) {
  return ge(e) ? e : new Sl(e, t);
}
class Sl {
  constructor(t, n) {
    (this.__v_isShallow = n),
      (this.dep = void 0),
      (this.__v_isRef = !0),
      (this._rawValue = n ? t : re(t)),
      (this._value = n ? t : Pn(t));
  }
  get value() {
    return gc(this), this._value;
  }
  set value(t) {
    const n = this.__v_isShallow || ao(t) || nn(t);
    (t = n ? t : re(t)),
      Tn(t, this._rawValue) &&
        ((this._rawValue = t), (this._value = n ? t : Pn(t)), _c(this));
  }
}
function z(e) {
  return ge(e) ? e.value : e;
}
const El = {
  get: (e, t, n) => z(Reflect.get(e, t, n)),
  set: (e, t, n, o) => {
    const s = e[t];
    return ge(s) && !ge(n) ? ((s.value = n), !0) : Reflect.set(e, t, n, o);
  },
};
function vc(e) {
  return xt(e) ? e : new Proxy(e, El);
}
function Ol(e) {
  const t = W(e) ? new Array(e.length) : {};
  for (const n in e) t[n] = Pl(e, n);
  return t;
}
class Tl {
  constructor(t, n, o) {
    (this._object = t),
      (this._key = n),
      (this._defaultValue = o),
      (this.__v_isRef = !0);
  }
  get value() {
    const t = this._object[this._key];
    return t === void 0 ? this._defaultValue : t;
  }
  set value(t) {
    this._object[this._key] = t;
  }
  get dep() {
    return el(re(this._object), this._key);
  }
}
function Pl(e, t, n) {
  const o = e[t];
  return ge(o) ? o : new Tl(e, t, n);
}
class Rl {
  constructor(t, n, o, s) {
    (this._setter = n),
      (this.dep = void 0),
      (this.__v_isRef = !0),
      (this.__v_isReadonly = !1),
      (this._dirty = !0),
      (this.effect = new Ms(t, () => {
        this._dirty || ((this._dirty = !0), _c(this));
      })),
      (this.effect.computed = this),
      (this.effect.active = this._cacheable = !s),
      (this.__v_isReadonly = o);
  }
  get value() {
    const t = re(this);
    return (
      gc(t),
      (t._dirty || !t._cacheable) &&
        ((t._dirty = !1), (t._value = t.effect.run())),
      t._value
    );
  }
  set value(t) {
    this._setter(t);
  }
}
function Al(e, t, n = !1) {
  let o, s;
  const r = Y(e);
  return (
    r ? ((o = e), (s = qe)) : ((o = e.get), (s = e.set)),
    new Rl(o, s, r || !s, n)
  );
}
function kt(e, t, n, o) {
  let s;
  try {
    s = o ? e(...o) : e();
  } catch (r) {
    xo(r, t, n);
  }
  return s;
}
function ze(e, t, n, o) {
  if (Y(e)) {
    const r = kt(e, t, n, o);
    return (
      r &&
        Gi(r) &&
        r.catch((i) => {
          xo(i, t, n);
        }),
      r
    );
  }
  const s = [];
  for (let r = 0; r < e.length; r++) s.push(ze(e[r], t, n, o));
  return s;
}
function xo(e, t, n, o = !0) {
  const s = t ? t.vnode : null;
  if (t) {
    let r = t.parent;
    const i = t.proxy,
      c = n;
    for (; r; ) {
      const l = r.ec;
      if (l) {
        for (let u = 0; u < l.length; u++) if (l[u](e, i, c) === !1) return;
      }
      r = r.parent;
    }
    const a = t.appContext.config.errorHandler;
    if (a) {
      kt(a, null, 10, [e, i, c]);
      return;
    }
  }
  jl(e, n, s, o);
}
function jl(e, t, n, o = !0) {
  console.error(e);
}
let Rn = !1,
  cs = !1;
const Re = [];
let tt = 0;
const tn = [];
let at = null,
  Lt = 0;
const bc = Promise.resolve();
let Hs = null;
function Bs(e) {
  const t = Hs || bc;
  return e ? t.then(this ? e.bind(this) : e) : t;
}
function $l(e) {
  let t = tt + 1,
    n = Re.length;
  for (; t < n; ) {
    const o = (t + n) >>> 1;
    An(Re[o]) < e ? (t = o + 1) : (n = o);
  }
  return t;
}
function Ws(e) {
  (!Re.length || !Re.includes(e, Rn && e.allowRecurse ? tt + 1 : tt)) &&
    (e.id == null ? Re.push(e) : Re.splice($l(e.id), 0, e), wc());
}
function wc() {
  !Rn && !cs && ((cs = !0), (Hs = bc.then(kc)));
}
function Ll(e) {
  const t = Re.indexOf(e);
  t > tt && Re.splice(t, 1);
}
function Nl(e) {
  W(e)
    ? tn.push(...e)
    : (!at || !at.includes(e, e.allowRecurse ? Lt + 1 : Lt)) && tn.push(e),
    wc();
}
function Er(e, t = Rn ? tt + 1 : 0) {
  for (; t < Re.length; t++) {
    const n = Re[t];
    n && n.pre && (Re.splice(t, 1), t--, n());
  }
}
function xc(e) {
  if (tn.length) {
    const t = [...new Set(tn)];
    if (((tn.length = 0), at)) {
      at.push(...t);
      return;
    }
    for (at = t, at.sort((n, o) => An(n) - An(o)), Lt = 0; Lt < at.length; Lt++)
      at[Lt]();
    (at = null), (Lt = 0);
  }
}
const An = (e) => (e.id == null ? 1 / 0 : e.id),
  Ml = (e, t) => {
    const n = An(e) - An(t);
    if (n === 0) {
      if (e.pre && !t.pre) return -1;
      if (t.pre && !e.pre) return 1;
    }
    return n;
  };
function kc(e) {
  (cs = !1), (Rn = !0), Re.sort(Ml);
  const t = qe;
  try {
    for (tt = 0; tt < Re.length; tt++) {
      const n = Re[tt];
      n && n.active !== !1 && kt(n, null, 14);
    }
  } finally {
    (tt = 0),
      (Re.length = 0),
      xc(),
      (Rn = !1),
      (Hs = null),
      (Re.length || tn.length) && kc();
  }
}
function Fl(e, t, ...n) {
  if (e.isUnmounted) return;
  const o = e.vnode.props || pe;
  let s = n;
  const r = t.startsWith("update:"),
    i = r && t.slice(7);
  if (i && i in o) {
    const u = `${i === "modelValue" ? "model" : i}Modifiers`,
      { number: f, trim: d } = o[u] || pe;
    d && (s = n.map((p) => (we(p) ? p.trim() : p))), f && (s = n.map(ns));
  }
  let c,
    a = o[(c = No(t))] || o[(c = No(ot(t)))];
  !a && r && (a = o[(c = No(Bt(t)))]), a && ze(a, e, 6, s);
  const l = o[c + "Once"];
  if (l) {
    if (!e.emitted) e.emitted = {};
    else if (e.emitted[c]) return;
    (e.emitted[c] = !0), ze(l, e, 6, s);
  }
}
function Cc(e, t, n = !1) {
  const o = t.emitsCache,
    s = o.get(e);
  if (s !== void 0) return s;
  const r = e.emits;
  let i = {},
    c = !1;
  if (!Y(e)) {
    const a = (l) => {
      const u = Cc(l, t, !0);
      u && ((c = !0), be(i, u));
    };
    !n && t.mixins.length && t.mixins.forEach(a),
      e.extends && a(e.extends),
      e.mixins && e.mixins.forEach(a);
  }
  return !r && !c
    ? (me(e) && o.set(e, null), null)
    : (W(r) ? r.forEach((a) => (i[a] = null)) : be(i, r),
      me(e) && o.set(e, i),
      i);
}
function ko(e, t) {
  return !e || !go(t)
    ? !1
    : ((t = t.slice(2).replace(/Once$/, "")),
      ie(e, t[0].toLowerCase() + t.slice(1)) || ie(e, Bt(t)) || ie(e, t));
}
let Te = null,
  Ic = null;
function lo(e) {
  const t = Te;
  return (Te = e), (Ic = (e && e.type.__scopeId) || null), t;
}
function rt(e, t = Te, n) {
  if (!t || e._n) return e;
  const o = (...s) => {
    o._d && Dr(-1);
    const r = lo(t);
    let i;
    try {
      i = e(...s);
    } finally {
      lo(r), o._d && Dr(1);
    }
    return i;
  };
  return (o._n = !0), (o._c = !0), (o._d = !0), o;
}
function Mo(e) {
  const {
    type: t,
    vnode: n,
    proxy: o,
    withProxy: s,
    props: r,
    propsOptions: [i],
    slots: c,
    attrs: a,
    emit: l,
    render: u,
    renderCache: f,
    data: d,
    setupState: p,
    ctx: g,
    inheritAttrs: y,
  } = e;
  let w, x;
  const v = lo(e);
  try {
    if (n.shapeFlag & 4) {
      const R = s || o;
      (w = Qe(u.call(R, R, f, r, p, d, g))), (x = a);
    } else {
      const R = t;
      (w = Qe(
        R.length > 1 ? R(r, { attrs: a, slots: c, emit: l }) : R(r, null)
      )),
        (x = t.props ? a : Dl(a));
    }
  } catch (R) {
    (kn.length = 0), xo(R, e, 1), (w = J(Ke));
  }
  let O = w;
  if (x && y !== !1) {
    const R = Object.keys(x),
      { shapeFlag: U } = O;
    R.length && U & 7 && (i && R.some(Rs) && (x = Ul(x, i)), (O = St(O, x)));
  }
  return (
    n.dirs && ((O = St(O)), (O.dirs = O.dirs ? O.dirs.concat(n.dirs) : n.dirs)),
    n.transition && (O.transition = n.transition),
    (w = O),
    lo(v),
    w
  );
}
const Dl = (e) => {
    let t;
    for (const n in e)
      (n === "class" || n === "style" || go(n)) && ((t || (t = {}))[n] = e[n]);
    return t;
  },
  Ul = (e, t) => {
    const n = {};
    for (const o in e) (!Rs(o) || !(o.slice(9) in t)) && (n[o] = e[o]);
    return n;
  };
function zl(e, t, n) {
  const { props: o, children: s, component: r } = e,
    { props: i, children: c, patchFlag: a } = t,
    l = r.emitsOptions;
  if (t.dirs || t.transition) return !0;
  if (n && a >= 0) {
    if (a & 1024) return !0;
    if (a & 16) return o ? Or(o, i, l) : !!i;
    if (a & 8) {
      const u = t.dynamicProps;
      for (let f = 0; f < u.length; f++) {
        const d = u[f];
        if (i[d] !== o[d] && !ko(l, d)) return !0;
      }
    }
  } else
    return (s || c) && (!c || !c.$stable)
      ? !0
      : o === i
      ? !1
      : o
      ? i
        ? Or(o, i, l)
        : !0
      : !!i;
  return !1;
}
function Or(e, t, n) {
  const o = Object.keys(t);
  if (o.length !== Object.keys(e).length) return !0;
  for (let s = 0; s < o.length; s++) {
    const r = o[s];
    if (t[r] !== e[r] && !ko(n, r)) return !0;
  }
  return !1;
}
function Kl({ vnode: e, parent: t }, n) {
  for (; t && t.subTree === e; ) ((e = t.vnode).el = n), (t = t.parent);
}
const Hl = (e) => e.__isSuspense;
function Bl(e, t) {
  t && t.pendingBranch
    ? W(e)
      ? t.effects.push(...e)
      : t.effects.push(e)
    : Nl(e);
}
function Sc(e, t) {
  return Vs(e, null, t);
}
const qn = {};
function Ee(e, t, n) {
  return Vs(e, t, n);
}
function Vs(
  e,
  t,
  { immediate: n, deep: o, flush: s, onTrack: r, onTrigger: i } = pe
) {
  var c;
  const a = Ls() === ((c = Se) == null ? void 0 : c.scope) ? Se : null;
  let l,
    u = !1,
    f = !1;
  if (
    (ge(e)
      ? ((l = () => e.value), (u = ao(e)))
      : xt(e)
      ? ((l = () => e), (o = !0))
      : W(e)
      ? ((f = !0),
        (u = e.some((R) => xt(R) || ao(R))),
        (l = () =>
          e.map((R) => {
            if (ge(R)) return R.value;
            if (xt(R)) return Ft(R);
            if (Y(R)) return kt(R, a, 2);
          })))
      : Y(e)
      ? t
        ? (l = () => kt(e, a, 2))
        : (l = () => {
            if (!(a && a.isUnmounted)) return d && d(), ze(e, a, 3, [p]);
          })
      : (l = qe),
    t && o)
  ) {
    const R = l;
    l = () => Ft(R());
  }
  let d,
    p = (R) => {
      d = v.onStop = () => {
        kt(R, a, 4);
      };
    },
    g;
  if ($n)
    if (
      ((p = qe),
      t ? n && ze(t, a, 3, [l(), f ? [] : void 0, p]) : l(),
      s === "sync")
    ) {
      const R = Fu();
      g = R.__watcherHandles || (R.__watcherHandles = []);
    } else return qe;
  let y = f ? new Array(e.length).fill(qn) : qn;
  const w = () => {
    if (v.active)
      if (t) {
        const R = v.run();
        (o || u || (f ? R.some((U, F) => Tn(U, y[F])) : Tn(R, y))) &&
          (d && d(),
          ze(t, a, 3, [R, y === qn ? void 0 : f && y[0] === qn ? [] : y, p]),
          (y = R));
      } else v.run();
  };
  w.allowRecurse = !!t;
  let x;
  s === "sync"
    ? (x = w)
    : s === "post"
    ? (x = () => Ne(w, a && a.suspense))
    : ((w.pre = !0), a && (w.id = a.uid), (x = () => Ws(w)));
  const v = new Ms(l, x);
  t
    ? n
      ? w()
      : (y = v.run())
    : s === "post"
    ? Ne(v.run.bind(v), a && a.suspense)
    : v.run();
  const O = () => {
    v.stop(), a && a.scope && As(a.scope.effects, v);
  };
  return g && g.push(O), O;
}
function Wl(e, t, n) {
  const o = this.proxy,
    s = we(e) ? (e.includes(".") ? Ec(o, e) : () => o[e]) : e.bind(o, o);
  let r;
  Y(t) ? (r = t) : ((r = t.handler), (n = t));
  const i = Se;
  sn(this);
  const c = Vs(s, r.bind(o), n);
  return i ? sn(i) : zt(), c;
}
function Ec(e, t) {
  const n = t.split(".");
  return () => {
    let o = e;
    for (let s = 0; s < n.length && o; s++) o = o[n[s]];
    return o;
  };
}
function Ft(e, t) {
  if (!me(e) || e.__v_skip || ((t = t || new Set()), t.has(e))) return e;
  if ((t.add(e), ge(e))) Ft(e.value, t);
  else if (W(e)) for (let n = 0; n < e.length; n++) Ft(e[n], t);
  else if (Ji(e) || en(e))
    e.forEach((n) => {
      Ft(n, t);
    });
  else if (Qi(e)) for (const n in e) Ft(e[n], t);
  return e;
}
function Oc(e, t) {
  const n = Te;
  if (n === null) return e;
  const o = Oo(n) || n.proxy,
    s = e.dirs || (e.dirs = []);
  for (let r = 0; r < t.length; r++) {
    let [i, c, a, l = pe] = t[r];
    i &&
      (Y(i) && (i = { mounted: i, updated: i }),
      i.deep && Ft(c),
      s.push({
        dir: i,
        instance: o,
        value: c,
        oldValue: void 0,
        arg: a,
        modifiers: l,
      }));
  }
  return e;
}
function Pt(e, t, n, o) {
  const s = e.dirs,
    r = t && t.dirs;
  for (let i = 0; i < s.length; i++) {
    const c = s[i];
    r && (c.oldValue = r[i].value);
    let a = c.dir[o];
    a && (an(), ze(a, n, 8, [e.el, c, e, t]), ln());
  }
}
function Vl() {
  const e = {
    isMounted: !1,
    isLeaving: !1,
    isUnmounting: !1,
    leavingVNodes: new Map(),
  };
  return (
    Un(() => {
      e.isMounted = !0;
    }),
    jc(() => {
      e.isUnmounting = !0;
    }),
    e
  );
}
const Ue = [Function, Array],
  Tc = {
    mode: String,
    appear: Boolean,
    persisted: Boolean,
    onBeforeEnter: Ue,
    onEnter: Ue,
    onAfterEnter: Ue,
    onEnterCancelled: Ue,
    onBeforeLeave: Ue,
    onLeave: Ue,
    onAfterLeave: Ue,
    onLeaveCancelled: Ue,
    onBeforeAppear: Ue,
    onAppear: Ue,
    onAfterAppear: Ue,
    onAppearCancelled: Ue,
  },
  Zl = {
    name: "BaseTransition",
    props: Tc,
    setup(e, { slots: t }) {
      const n = Vc(),
        o = Vl();
      let s;
      return () => {
        const r = t.default && Rc(t.default(), !0);
        if (!r || !r.length) return;
        let i = r[0];
        if (r.length > 1) {
          for (const y of r)
            if (y.type !== Ke) {
              i = y;
              break;
            }
        }
        const c = re(e),
          { mode: a } = c;
        if (o.isLeaving) return Fo(i);
        const l = Tr(i);
        if (!l) return Fo(i);
        const u = as(l, c, o, n);
        ls(l, u);
        const f = n.subTree,
          d = f && Tr(f);
        let p = !1;
        const { getTransitionKey: g } = l.type;
        if (g) {
          const y = g();
          s === void 0 ? (s = y) : y !== s && ((s = y), (p = !0));
        }
        if (d && d.type !== Ke && (!Nt(l, d) || p)) {
          const y = as(d, c, o, n);
          if ((ls(d, y), a === "out-in"))
            return (
              (o.isLeaving = !0),
              (y.afterLeave = () => {
                (o.isLeaving = !1), n.update.active !== !1 && n.update();
              }),
              Fo(i)
            );
          a === "in-out" &&
            l.type !== Ke &&
            (y.delayLeave = (w, x, v) => {
              const O = Pc(o, d);
              (O[String(d.key)] = d),
                (w._leaveCb = () => {
                  x(), (w._leaveCb = void 0), delete u.delayedLeave;
                }),
                (u.delayedLeave = v);
            });
        }
        return i;
      };
    },
  },
  ql = Zl;
function Pc(e, t) {
  const { leavingVNodes: n } = e;
  let o = n.get(t.type);
  return o || ((o = Object.create(null)), n.set(t.type, o)), o;
}
function as(e, t, n, o) {
  const {
      appear: s,
      mode: r,
      persisted: i = !1,
      onBeforeEnter: c,
      onEnter: a,
      onAfterEnter: l,
      onEnterCancelled: u,
      onBeforeLeave: f,
      onLeave: d,
      onAfterLeave: p,
      onLeaveCancelled: g,
      onBeforeAppear: y,
      onAppear: w,
      onAfterAppear: x,
      onAppearCancelled: v,
    } = t,
    O = String(e.key),
    R = Pc(n, e),
    U = (T, Z) => {
      T && ze(T, o, 9, Z);
    },
    F = (T, Z) => {
      const q = Z[1];
      U(T, Z),
        W(T) ? T.every((ae) => ae.length <= 1) && q() : T.length <= 1 && q();
    },
    N = {
      mode: r,
      persisted: i,
      beforeEnter(T) {
        let Z = c;
        if (!n.isMounted)
          if (s) Z = y || c;
          else return;
        T._leaveCb && T._leaveCb(!0);
        const q = R[O];
        q && Nt(e, q) && q.el._leaveCb && q.el._leaveCb(), U(Z, [T]);
      },
      enter(T) {
        let Z = a,
          q = l,
          ae = u;
        if (!n.isMounted)
          if (s) (Z = w || a), (q = x || l), (ae = v || u);
          else return;
        let L = !1;
        const oe = (T._enterCb = (de) => {
          L ||
            ((L = !0),
            de ? U(ae, [T]) : U(q, [T]),
            N.delayedLeave && N.delayedLeave(),
            (T._enterCb = void 0));
        });
        Z ? F(Z, [T, oe]) : oe();
      },
      leave(T, Z) {
        const q = String(e.key);
        if ((T._enterCb && T._enterCb(!0), n.isUnmounting)) return Z();
        U(f, [T]);
        let ae = !1;
        const L = (T._leaveCb = (oe) => {
          ae ||
            ((ae = !0),
            Z(),
            oe ? U(g, [T]) : U(p, [T]),
            (T._leaveCb = void 0),
            R[q] === e && delete R[q]);
        });
        (R[q] = e), d ? F(d, [T, L]) : L();
      },
      clone(T) {
        return as(T, t, n, o);
      },
    };
  return N;
}
function Fo(e) {
  if (Co(e)) return (e = St(e)), (e.children = null), e;
}
function Tr(e) {
  return Co(e) ? (e.children ? e.children[0] : void 0) : e;
}
function ls(e, t) {
  e.shapeFlag & 6 && e.component
    ? ls(e.component.subTree, t)
    : e.shapeFlag & 128
    ? ((e.ssContent.transition = t.clone(e.ssContent)),
      (e.ssFallback.transition = t.clone(e.ssFallback)))
    : (e.transition = t);
}
function Rc(e, t = !1, n) {
  let o = [],
    s = 0;
  for (let r = 0; r < e.length; r++) {
    let i = e[r];
    const c = n == null ? i.key : String(n) + String(i.key != null ? i.key : r);
    i.type === _e
      ? (i.patchFlag & 128 && s++, (o = o.concat(Rc(i.children, t, c))))
      : (t || i.type !== Ke) && o.push(c != null ? St(i, { key: c }) : i);
  }
  if (s > 1) for (let r = 0; r < o.length; r++) o[r].patchFlag = -2;
  return o;
}
function $e(e, t) {
  return Y(e) ? (() => be({ name: e.name }, t, { setup: e }))() : e;
}
const wn = (e) => !!e.type.__asyncLoader,
  Co = (e) => e.type.__isKeepAlive;
function Xl(e, t) {
  Ac(e, "a", t);
}
function Jl(e, t) {
  Ac(e, "da", t);
}
function Ac(e, t, n = Se) {
  const o =
    e.__wdc ||
    (e.__wdc = () => {
      let s = n;
      for (; s; ) {
        if (s.isDeactivated) return;
        s = s.parent;
      }
      return e();
    });
  if ((Io(t, o, n), n)) {
    let s = n.parent;
    for (; s && s.parent; )
      Co(s.parent.vnode) && Gl(o, t, n, s), (s = s.parent);
  }
}
function Gl(e, t, n, o) {
  const s = Io(t, e, o, !0);
  Zs(() => {
    As(o[t], s);
  }, n);
}
function Io(e, t, n = Se, o = !1) {
  if (n) {
    const s = n[e] || (n[e] = []),
      r =
        t.__weh ||
        (t.__weh = (...i) => {
          if (n.isUnmounted) return;
          an(), sn(n);
          const c = ze(t, n, e, i);
          return zt(), ln(), c;
        });
    return o ? s.unshift(r) : s.push(r), r;
  }
}
const dt =
    (e) =>
    (t, n = Se) =>
      (!$n || e === "sp") && Io(e, (...o) => t(...o), n),
  Yl = dt("bm"),
  Un = dt("m"),
  Ql = dt("bu"),
  eu = dt("u"),
  jc = dt("bum"),
  Zs = dt("um"),
  tu = dt("sp"),
  nu = dt("rtg"),
  ou = dt("rtc");
function su(e, t = Se) {
  Io("ec", e, t);
}
const $c = "components";
function It(e, t) {
  return iu($c, e, !0, t) || e;
}
const ru = Symbol.for("v-ndc");
function iu(e, t, n = !0, o = !1) {
  const s = Te || Se;
  if (s) {
    const r = s.type;
    if (e === $c) {
      const c = Lu(r, !1);
      if (c && (c === t || c === ot(t) || c === vo(ot(t)))) return r;
    }
    const i = Pr(s[e] || r[e], t) || Pr(s.appContext[e], t);
    return !i && o ? r : i;
  }
}
function Pr(e, t) {
  return e && (e[t] || e[ot(t)] || e[vo(ot(t))]);
}
function zn(e, t, n, o) {
  let s;
  const r = n && n[o];
  if (W(e) || we(e)) {
    s = new Array(e.length);
    for (let i = 0, c = e.length; i < c; i++)
      s[i] = t(e[i], i, void 0, r && r[i]);
  } else if (typeof e == "number") {
    s = new Array(e);
    for (let i = 0; i < e; i++) s[i] = t(i + 1, i, void 0, r && r[i]);
  } else if (me(e))
    if (e[Symbol.iterator])
      s = Array.from(e, (i, c) => t(i, c, void 0, r && r[c]));
    else {
      const i = Object.keys(e);
      s = new Array(i.length);
      for (let c = 0, a = i.length; c < a; c++) {
        const l = i[c];
        s[c] = t(e[l], l, c, r && r[c]);
      }
    }
  else s = [];
  return n && (n[o] = s), s;
}
function ut(e, t, n = {}, o, s) {
  if (Te.isCE || (Te.parent && wn(Te.parent) && Te.parent.isCE))
    return t !== "default" && (n.name = t), J("slot", n, o && o());
  let r = e[t];
  r && r._c && (r._d = !1), V();
  const i = r && Lc(r(n)),
    c = Wt(
      _e,
      { key: n.key || (i && i.key) || `_${t}` },
      i || (o ? o() : []),
      i && e._ === 1 ? 64 : -2
    );
  return (
    !s && c.scopeId && (c.slotScopeIds = [c.scopeId + "-s"]),
    r && r._c && (r._d = !0),
    c
  );
}
function Lc(e) {
  return e.some((t) =>
    ho(t) ? !(t.type === Ke || (t.type === _e && !Lc(t.children))) : !0
  )
    ? e
    : null;
}
const us = (e) => (e ? (Zc(e) ? Oo(e) || e.proxy : us(e.parent)) : null),
  xn = be(Object.create(null), {
    $: (e) => e,
    $el: (e) => e.vnode.el,
    $data: (e) => e.data,
    $props: (e) => e.props,
    $attrs: (e) => e.attrs,
    $slots: (e) => e.slots,
    $refs: (e) => e.refs,
    $parent: (e) => us(e.parent),
    $root: (e) => us(e.root),
    $emit: (e) => e.emit,
    $options: (e) => qs(e),
    $forceUpdate: (e) => e.f || (e.f = () => Ws(e.update)),
    $nextTick: (e) => e.n || (e.n = Bs.bind(e.proxy)),
    $watch: (e) => Wl.bind(e),
  }),
  Do = (e, t) => e !== pe && !e.__isScriptSetup && ie(e, t),
  cu = {
    get({ _: e }, t) {
      const {
        ctx: n,
        setupState: o,
        data: s,
        props: r,
        accessCache: i,
        type: c,
        appContext: a,
      } = e;
      let l;
      if (t[0] !== "$") {
        const p = i[t];
        if (p !== void 0)
          switch (p) {
            case 1:
              return o[t];
            case 2:
              return s[t];
            case 4:
              return n[t];
            case 3:
              return r[t];
          }
        else {
          if (Do(o, t)) return (i[t] = 1), o[t];
          if (s !== pe && ie(s, t)) return (i[t] = 2), s[t];
          if ((l = e.propsOptions[0]) && ie(l, t)) return (i[t] = 3), r[t];
          if (n !== pe && ie(n, t)) return (i[t] = 4), n[t];
          fs && (i[t] = 0);
        }
      }
      const u = xn[t];
      let f, d;
      if (u) return t === "$attrs" && Me(e, "get", t), u(e);
      if ((f = c.__cssModules) && (f = f[t])) return f;
      if (n !== pe && ie(n, t)) return (i[t] = 4), n[t];
      if (((d = a.config.globalProperties), ie(d, t))) return d[t];
    },
    set({ _: e }, t, n) {
      const { data: o, setupState: s, ctx: r } = e;
      return Do(s, t)
        ? ((s[t] = n), !0)
        : o !== pe && ie(o, t)
        ? ((o[t] = n), !0)
        : ie(e.props, t) || (t[0] === "$" && t.slice(1) in e)
        ? !1
        : ((r[t] = n), !0);
    },
    has(
      {
        _: {
          data: e,
          setupState: t,
          accessCache: n,
          ctx: o,
          appContext: s,
          propsOptions: r,
        },
      },
      i
    ) {
      let c;
      return (
        !!n[i] ||
        (e !== pe && ie(e, i)) ||
        Do(t, i) ||
        ((c = r[0]) && ie(c, i)) ||
        ie(o, i) ||
        ie(xn, i) ||
        ie(s.config.globalProperties, i)
      );
    },
    defineProperty(e, t, n) {
      return (
        n.get != null
          ? (e._.accessCache[t] = 0)
          : ie(n, "value") && this.set(e, t, n.value, null),
        Reflect.defineProperty(e, t, n)
      );
    },
  };
function Rr(e) {
  return W(e) ? e.reduce((t, n) => ((t[n] = null), t), {}) : e;
}
let fs = !0;
function au(e) {
  const t = qs(e),
    n = e.proxy,
    o = e.ctx;
  (fs = !1), t.beforeCreate && Ar(t.beforeCreate, e, "bc");
  const {
    data: s,
    computed: r,
    methods: i,
    watch: c,
    provide: a,
    inject: l,
    created: u,
    beforeMount: f,
    mounted: d,
    beforeUpdate: p,
    updated: g,
    activated: y,
    deactivated: w,
    beforeDestroy: x,
    beforeUnmount: v,
    destroyed: O,
    unmounted: R,
    render: U,
    renderTracked: F,
    renderTriggered: N,
    errorCaptured: T,
    serverPrefetch: Z,
    expose: q,
    inheritAttrs: ae,
    components: L,
    directives: oe,
    filters: de,
  } = t;
  if ((l && lu(l, o, null), i))
    for (const Q in i) {
      const te = i[Q];
      Y(te) && (o[Q] = te.bind(n));
    }
  if (s) {
    const Q = s.call(n, n);
    me(Q) && (e.data = st(Q));
  }
  if (((fs = !0), r))
    for (const Q in r) {
      const te = r[Q],
        xe = Y(te) ? te.bind(n, n) : Y(te.get) ? te.get.bind(n, n) : qe,
        Ie = !Y(te) && Y(te.set) ? te.set.bind(n) : qe,
        Ae = Oe({ get: xe, set: Ie });
      Object.defineProperty(o, Q, {
        enumerable: !0,
        configurable: !0,
        get: () => Ae.value,
        set: (ke) => (Ae.value = ke),
      });
    }
  if (c) for (const Q in c) Nc(c[Q], o, n, Q);
  if (a) {
    const Q = Y(a) ? a.call(n) : a;
    Reflect.ownKeys(Q).forEach((te) => {
      eo(te, Q[te]);
    });
  }
  u && Ar(u, e, "c");
  function ce(Q, te) {
    W(te) ? te.forEach((xe) => Q(xe.bind(n))) : te && Q(te.bind(n));
  }
  if (
    (ce(Yl, f),
    ce(Un, d),
    ce(Ql, p),
    ce(eu, g),
    ce(Xl, y),
    ce(Jl, w),
    ce(su, T),
    ce(ou, F),
    ce(nu, N),
    ce(jc, v),
    ce(Zs, R),
    ce(tu, Z),
    W(q))
  )
    if (q.length) {
      const Q = e.exposed || (e.exposed = {});
      q.forEach((te) => {
        Object.defineProperty(Q, te, {
          get: () => n[te],
          set: (xe) => (n[te] = xe),
        });
      });
    } else e.exposed || (e.exposed = {});
  U && e.render === qe && (e.render = U),
    ae != null && (e.inheritAttrs = ae),
    L && (e.components = L),
    oe && (e.directives = oe);
}
function lu(e, t, n = qe) {
  W(e) && (e = ds(e));
  for (const o in e) {
    const s = e[o];
    let r;
    me(s)
      ? "default" in s
        ? (r = Xe(s.from || o, s.default, !0))
        : (r = Xe(s.from || o))
      : (r = Xe(s)),
      ge(r)
        ? Object.defineProperty(t, o, {
            enumerable: !0,
            configurable: !0,
            get: () => r.value,
            set: (i) => (r.value = i),
          })
        : (t[o] = r);
  }
}
function Ar(e, t, n) {
  ze(W(e) ? e.map((o) => o.bind(t.proxy)) : e.bind(t.proxy), t, n);
}
function Nc(e, t, n, o) {
  const s = o.includes(".") ? Ec(n, o) : () => n[o];
  if (we(e)) {
    const r = t[e];
    Y(r) && Ee(s, r);
  } else if (Y(e)) Ee(s, e.bind(n));
  else if (me(e))
    if (W(e)) e.forEach((r) => Nc(r, t, n, o));
    else {
      const r = Y(e.handler) ? e.handler.bind(n) : t[e.handler];
      Y(r) && Ee(s, r, e);
    }
}
function qs(e) {
  const t = e.type,
    { mixins: n, extends: o } = t,
    {
      mixins: s,
      optionsCache: r,
      config: { optionMergeStrategies: i },
    } = e.appContext,
    c = r.get(t);
  let a;
  return (
    c
      ? (a = c)
      : !s.length && !n && !o
      ? (a = t)
      : ((a = {}), s.length && s.forEach((l) => uo(a, l, i, !0)), uo(a, t, i)),
    me(t) && r.set(t, a),
    a
  );
}
function uo(e, t, n, o = !1) {
  const { mixins: s, extends: r } = t;
  r && uo(e, r, n, !0), s && s.forEach((i) => uo(e, i, n, !0));
  for (const i in t)
    if (!(o && i === "expose")) {
      const c = uu[i] || (n && n[i]);
      e[i] = c ? c(e[i], t[i]) : t[i];
    }
  return e;
}
const uu = {
  data: jr,
  props: $r,
  emits: $r,
  methods: yn,
  computed: yn,
  beforeCreate: je,
  created: je,
  beforeMount: je,
  mounted: je,
  beforeUpdate: je,
  updated: je,
  beforeDestroy: je,
  beforeUnmount: je,
  destroyed: je,
  unmounted: je,
  activated: je,
  deactivated: je,
  errorCaptured: je,
  serverPrefetch: je,
  components: yn,
  directives: yn,
  watch: du,
  provide: jr,
  inject: fu,
};
function jr(e, t) {
  return t
    ? e
      ? function () {
          return be(
            Y(e) ? e.call(this, this) : e,
            Y(t) ? t.call(this, this) : t
          );
        }
      : t
    : e;
}
function fu(e, t) {
  return yn(ds(e), ds(t));
}
function ds(e) {
  if (W(e)) {
    const t = {};
    for (let n = 0; n < e.length; n++) t[e[n]] = e[n];
    return t;
  }
  return e;
}
function je(e, t) {
  return e ? [...new Set([].concat(e, t))] : t;
}
function yn(e, t) {
  return e ? be(Object.create(null), e, t) : t;
}
function $r(e, t) {
  return e
    ? W(e) && W(t)
      ? [...new Set([...e, ...t])]
      : be(Object.create(null), Rr(e), Rr(t ?? {}))
    : t;
}
function du(e, t) {
  if (!e) return t;
  if (!t) return e;
  const n = be(Object.create(null), e);
  for (const o in t) n[o] = je(e[o], t[o]);
  return n;
}
function Mc() {
  return {
    app: null,
    config: {
      isNativeTag: Fa,
      performance: !1,
      globalProperties: {},
      optionMergeStrategies: {},
      errorHandler: void 0,
      warnHandler: void 0,
      compilerOptions: {},
    },
    mixins: [],
    components: {},
    directives: {},
    provides: Object.create(null),
    optionsCache: new WeakMap(),
    propsCache: new WeakMap(),
    emitsCache: new WeakMap(),
  };
}
let hu = 0;
function pu(e, t) {
  return function (o, s = null) {
    Y(o) || (o = be({}, o)), s != null && !me(s) && (s = null);
    const r = Mc(),
      i = new Set();
    let c = !1;
    const a = (r.app = {
      _uid: hu++,
      _component: o,
      _props: s,
      _container: null,
      _context: r,
      _instance: null,
      version: Du,
      get config() {
        return r.config;
      },
      set config(l) {},
      use(l, ...u) {
        return (
          i.has(l) ||
            (l && Y(l.install)
              ? (i.add(l), l.install(a, ...u))
              : Y(l) && (i.add(l), l(a, ...u))),
          a
        );
      },
      mixin(l) {
        return r.mixins.includes(l) || r.mixins.push(l), a;
      },
      component(l, u) {
        return u ? ((r.components[l] = u), a) : r.components[l];
      },
      directive(l, u) {
        return u ? ((r.directives[l] = u), a) : r.directives[l];
      },
      mount(l, u, f) {
        if (!c) {
          const d = J(o, s);
          return (
            (d.appContext = r),
            u && t ? t(d, l) : e(d, l, f),
            (c = !0),
            (a._container = l),
            (l.__vue_app__ = a),
            Oo(d.component) || d.component.proxy
          );
        }
      },
      unmount() {
        c && (e(null, a._container), delete a._container.__vue_app__);
      },
      provide(l, u) {
        return (r.provides[l] = u), a;
      },
      runWithContext(l) {
        fo = a;
        try {
          return l();
        } finally {
          fo = null;
        }
      },
    });
    return a;
  };
}
let fo = null;
function eo(e, t) {
  if (Se) {
    let n = Se.provides;
    const o = Se.parent && Se.parent.provides;
    o === n && (n = Se.provides = Object.create(o)), (n[e] = t);
  }
}
function Xe(e, t, n = !1) {
  const o = Se || Te;
  if (o || fo) {
    const s = o
      ? o.parent == null
        ? o.vnode.appContext && o.vnode.appContext.provides
        : o.parent.provides
      : fo._context.provides;
    if (s && e in s) return s[e];
    if (arguments.length > 1) return n && Y(t) ? t.call(o && o.proxy) : t;
  }
}
function mu(e, t, n, o = !1) {
  const s = {},
    r = {};
  io(r, Eo, 1), (e.propsDefaults = Object.create(null)), Fc(e, t, s, r);
  for (const i in e.propsOptions[0]) i in s || (s[i] = void 0);
  n ? (e.props = o ? s : Il(s)) : e.type.props ? (e.props = s) : (e.props = r),
    (e.attrs = r);
}
function gu(e, t, n, o) {
  const {
      props: s,
      attrs: r,
      vnode: { patchFlag: i },
    } = e,
    c = re(s),
    [a] = e.propsOptions;
  let l = !1;
  if ((o || i > 0) && !(i & 16)) {
    if (i & 8) {
      const u = e.vnode.dynamicProps;
      for (let f = 0; f < u.length; f++) {
        let d = u[f];
        if (ko(e.emitsOptions, d)) continue;
        const p = t[d];
        if (a)
          if (ie(r, d)) p !== r[d] && ((r[d] = p), (l = !0));
          else {
            const g = ot(d);
            s[g] = hs(a, c, g, p, e, !1);
          }
        else p !== r[d] && ((r[d] = p), (l = !0));
      }
    }
  } else {
    Fc(e, t, s, r) && (l = !0);
    let u;
    for (const f in c)
      (!t || (!ie(t, f) && ((u = Bt(f)) === f || !ie(t, u)))) &&
        (a
          ? n &&
            (n[f] !== void 0 || n[u] !== void 0) &&
            (s[f] = hs(a, c, f, void 0, e, !0))
          : delete s[f]);
    if (r !== c)
      for (const f in r) (!t || !ie(t, f)) && (delete r[f], (l = !0));
  }
  l && ft(e, "set", "$attrs");
}
function Fc(e, t, n, o) {
  const [s, r] = e.propsOptions;
  let i = !1,
    c;
  if (t)
    for (let a in t) {
      if (Gn(a)) continue;
      const l = t[a];
      let u;
      s && ie(s, (u = ot(a)))
        ? !r || !r.includes(u)
          ? (n[u] = l)
          : ((c || (c = {}))[u] = l)
        : ko(e.emitsOptions, a) ||
          ((!(a in o) || l !== o[a]) && ((o[a] = l), (i = !0)));
    }
  if (r) {
    const a = re(n),
      l = c || pe;
    for (let u = 0; u < r.length; u++) {
      const f = r[u];
      n[f] = hs(s, a, f, l[f], e, !ie(l, f));
    }
  }
  return i;
}
function hs(e, t, n, o, s, r) {
  const i = e[n];
  if (i != null) {
    const c = ie(i, "default");
    if (c && o === void 0) {
      const a = i.default;
      if (i.type !== Function && !i.skipFactory && Y(a)) {
        const { propsDefaults: l } = s;
        n in l ? (o = l[n]) : (sn(s), (o = l[n] = a.call(null, t)), zt());
      } else o = a;
    }
    i[0] &&
      (r && !c ? (o = !1) : i[1] && (o === "" || o === Bt(n)) && (o = !0));
  }
  return o;
}
function Dc(e, t, n = !1) {
  const o = t.propsCache,
    s = o.get(e);
  if (s) return s;
  const r = e.props,
    i = {},
    c = [];
  let a = !1;
  if (!Y(e)) {
    const u = (f) => {
      a = !0;
      const [d, p] = Dc(f, t, !0);
      be(i, d), p && c.push(...p);
    };
    !n && t.mixins.length && t.mixins.forEach(u),
      e.extends && u(e.extends),
      e.mixins && e.mixins.forEach(u);
  }
  if (!r && !a) return me(e) && o.set(e, Qt), Qt;
  if (W(r))
    for (let u = 0; u < r.length; u++) {
      const f = ot(r[u]);
      Lr(f) && (i[f] = pe);
    }
  else if (r)
    for (const u in r) {
      const f = ot(u);
      if (Lr(f)) {
        const d = r[u],
          p = (i[f] = W(d) || Y(d) ? { type: d } : be({}, d));
        if (p) {
          const g = Fr(Boolean, p.type),
            y = Fr(String, p.type);
          (p[0] = g > -1),
            (p[1] = y < 0 || g < y),
            (g > -1 || ie(p, "default")) && c.push(f);
        }
      }
    }
  const l = [i, c];
  return me(e) && o.set(e, l), l;
}
function Lr(e) {
  return e[0] !== "$";
}
function Nr(e) {
  const t = e && e.toString().match(/^\s*(function|class) (\w+)/);
  return t ? t[2] : e === null ? "null" : "";
}
function Mr(e, t) {
  return Nr(e) === Nr(t);
}
function Fr(e, t) {
  return W(t) ? t.findIndex((n) => Mr(n, e)) : Y(t) && Mr(t, e) ? 0 : -1;
}
const Uc = (e) => e[0] === "_" || e === "$stable",
  Xs = (e) => (W(e) ? e.map(Qe) : [Qe(e)]),
  _u = (e, t, n) => {
    if (t._n) return t;
    const o = rt((...s) => Xs(t(...s)), n);
    return (o._c = !1), o;
  },
  zc = (e, t, n) => {
    const o = e._ctx;
    for (const s in e) {
      if (Uc(s)) continue;
      const r = e[s];
      if (Y(r)) t[s] = _u(s, r, o);
      else if (r != null) {
        const i = Xs(r);
        t[s] = () => i;
      }
    }
  },
  Kc = (e, t) => {
    const n = Xs(t);
    e.slots.default = () => n;
  },
  yu = (e, t) => {
    if (e.vnode.shapeFlag & 32) {
      const n = t._;
      n ? ((e.slots = re(t)), io(t, "_", n)) : zc(t, (e.slots = {}));
    } else (e.slots = {}), t && Kc(e, t);
    io(e.slots, Eo, 1);
  },
  vu = (e, t, n) => {
    const { vnode: o, slots: s } = e;
    let r = !0,
      i = pe;
    if (o.shapeFlag & 32) {
      const c = t._;
      c
        ? n && c === 1
          ? (r = !1)
          : (be(s, t), !n && c === 1 && delete s._)
        : ((r = !t.$stable), zc(t, s)),
        (i = t);
    } else t && (Kc(e, t), (i = { default: 1 }));
    if (r) for (const c in s) !Uc(c) && !(c in i) && delete s[c];
  };
function ps(e, t, n, o, s = !1) {
  if (W(e)) {
    e.forEach((d, p) => ps(d, t && (W(t) ? t[p] : t), n, o, s));
    return;
  }
  if (wn(o) && !s) return;
  const r = o.shapeFlag & 4 ? Oo(o.component) || o.component.proxy : o.el,
    i = s ? null : r,
    { i: c, r: a } = e,
    l = t && t.r,
    u = c.refs === pe ? (c.refs = {}) : c.refs,
    f = c.setupState;
  if (
    (l != null &&
      l !== a &&
      (we(l)
        ? ((u[l] = null), ie(f, l) && (f[l] = null))
        : ge(l) && (l.value = null)),
    Y(a))
  )
    kt(a, c, 12, [i, u]);
  else {
    const d = we(a),
      p = ge(a);
    if (d || p) {
      const g = () => {
        if (e.f) {
          const y = d ? (ie(f, a) ? f[a] : u[a]) : a.value;
          s
            ? W(y) && As(y, r)
            : W(y)
            ? y.includes(r) || y.push(r)
            : d
            ? ((u[a] = [r]), ie(f, a) && (f[a] = u[a]))
            : ((a.value = [r]), e.k && (u[e.k] = a.value));
        } else
          d
            ? ((u[a] = i), ie(f, a) && (f[a] = i))
            : p && ((a.value = i), e.k && (u[e.k] = i));
      };
      i ? ((g.id = -1), Ne(g, n)) : g();
    }
  }
}
const Ne = Bl;
function bu(e) {
  return wu(e);
}
function wu(e, t) {
  const n = os();
  n.__VUE__ = !0;
  const {
      insert: o,
      remove: s,
      patchProp: r,
      createElement: i,
      createText: c,
      createComment: a,
      setText: l,
      setElementText: u,
      parentNode: f,
      nextSibling: d,
      setScopeId: p = qe,
      insertStaticContent: g,
    } = e,
    y = (
      h,
      m,
      _,
      b = null,
      C = null,
      I = null,
      $ = !1,
      P = null,
      A = !!m.dynamicChildren
    ) => {
      if (h === m) return;
      h && !Nt(h, m) && ((b = k(h)), ke(h, C, I, !0), (h = null)),
        m.patchFlag === -2 && ((A = !1), (m.dynamicChildren = null));
      const { type: S, ref: H, shapeFlag: D } = m;
      switch (S) {
        case So:
          w(h, m, _, b);
          break;
        case Ke:
          x(h, m, _, b);
          break;
        case Uo:
          h == null && v(m, _, b, $);
          break;
        case _e:
          L(h, m, _, b, C, I, $, P, A);
          break;
        default:
          D & 1
            ? U(h, m, _, b, C, I, $, P, A)
            : D & 6
            ? oe(h, m, _, b, C, I, $, P, A)
            : (D & 64 || D & 128) && S.process(h, m, _, b, C, I, $, P, A, j);
      }
      H != null && C && ps(H, h && h.ref, I, m || h, !m);
    },
    w = (h, m, _, b) => {
      if (h == null) o((m.el = c(m.children)), _, b);
      else {
        const C = (m.el = h.el);
        m.children !== h.children && l(C, m.children);
      }
    },
    x = (h, m, _, b) => {
      h == null ? o((m.el = a(m.children || "")), _, b) : (m.el = h.el);
    },
    v = (h, m, _, b) => {
      [h.el, h.anchor] = g(h.children, m, _, b, h.el, h.anchor);
    },
    O = ({ el: h, anchor: m }, _, b) => {
      let C;
      for (; h && h !== m; ) (C = d(h)), o(h, _, b), (h = C);
      o(m, _, b);
    },
    R = ({ el: h, anchor: m }) => {
      let _;
      for (; h && h !== m; ) (_ = d(h)), s(h), (h = _);
      s(m);
    },
    U = (h, m, _, b, C, I, $, P, A) => {
      ($ = $ || m.type === "svg"),
        h == null ? F(m, _, b, C, I, $, P, A) : Z(h, m, C, I, $, P, A);
    },
    F = (h, m, _, b, C, I, $, P) => {
      let A, S;
      const { type: H, props: D, shapeFlag: B, transition: X, dirs: ne } = h;
      if (
        ((A = h.el = i(h.type, I, D && D.is, D)),
        B & 8
          ? u(A, h.children)
          : B & 16 &&
            T(h.children, A, null, b, C, I && H !== "foreignObject", $, P),
        ne && Pt(h, null, b, "created"),
        N(A, h, h.scopeId, $, b),
        D)
      ) {
        for (const fe in D)
          fe !== "value" &&
            !Gn(fe) &&
            r(A, fe, null, D[fe], I, h.children, b, C, Pe);
        "value" in D && r(A, "value", null, D.value),
          (S = D.onVnodeBeforeMount) && Ye(S, b, h);
      }
      ne && Pt(h, null, b, "beforeMount");
      const he = (!C || (C && !C.pendingBranch)) && X && !X.persisted;
      he && X.beforeEnter(A),
        o(A, m, _),
        ((S = D && D.onVnodeMounted) || he || ne) &&
          Ne(() => {
            S && Ye(S, b, h), he && X.enter(A), ne && Pt(h, null, b, "mounted");
          }, C);
    },
    N = (h, m, _, b, C) => {
      if ((_ && p(h, _), b)) for (let I = 0; I < b.length; I++) p(h, b[I]);
      if (C) {
        let I = C.subTree;
        if (m === I) {
          const $ = C.vnode;
          N(h, $, $.scopeId, $.slotScopeIds, C.parent);
        }
      }
    },
    T = (h, m, _, b, C, I, $, P, A = 0) => {
      for (let S = A; S < h.length; S++) {
        const H = (h[S] = P ? vt(h[S]) : Qe(h[S]));
        y(null, H, m, _, b, C, I, $, P);
      }
    },
    Z = (h, m, _, b, C, I, $) => {
      const P = (m.el = h.el);
      let { patchFlag: A, dynamicChildren: S, dirs: H } = m;
      A |= h.patchFlag & 16;
      const D = h.props || pe,
        B = m.props || pe;
      let X;
      _ && Rt(_, !1),
        (X = B.onVnodeBeforeUpdate) && Ye(X, _, m, h),
        H && Pt(m, h, _, "beforeUpdate"),
        _ && Rt(_, !0);
      const ne = C && m.type !== "foreignObject";
      if (
        (S
          ? q(h.dynamicChildren, S, P, _, b, ne, I)
          : $ || te(h, m, P, null, _, b, ne, I, !1),
        A > 0)
      ) {
        if (A & 16) ae(P, m, D, B, _, b, C);
        else if (
          (A & 2 && D.class !== B.class && r(P, "class", null, B.class, C),
          A & 4 && r(P, "style", D.style, B.style, C),
          A & 8)
        ) {
          const he = m.dynamicProps;
          for (let fe = 0; fe < he.length; fe++) {
            const ve = he[fe],
              Be = D[ve],
              Vt = B[ve];
            (Vt !== Be || ve === "value") &&
              r(P, ve, Be, Vt, C, h.children, _, b, Pe);
          }
        }
        A & 1 && h.children !== m.children && u(P, m.children);
      } else !$ && S == null && ae(P, m, D, B, _, b, C);
      ((X = B.onVnodeUpdated) || H) &&
        Ne(() => {
          X && Ye(X, _, m, h), H && Pt(m, h, _, "updated");
        }, b);
    },
    q = (h, m, _, b, C, I, $) => {
      for (let P = 0; P < m.length; P++) {
        const A = h[P],
          S = m[P],
          H =
            A.el && (A.type === _e || !Nt(A, S) || A.shapeFlag & 70)
              ? f(A.el)
              : _;
        y(A, S, H, null, b, C, I, $, !0);
      }
    },
    ae = (h, m, _, b, C, I, $) => {
      if (_ !== b) {
        if (_ !== pe)
          for (const P in _)
            !Gn(P) && !(P in b) && r(h, P, _[P], null, $, m.children, C, I, Pe);
        for (const P in b) {
          if (Gn(P)) continue;
          const A = b[P],
            S = _[P];
          A !== S && P !== "value" && r(h, P, S, A, $, m.children, C, I, Pe);
        }
        "value" in b && r(h, "value", _.value, b.value);
      }
    },
    L = (h, m, _, b, C, I, $, P, A) => {
      const S = (m.el = h ? h.el : c("")),
        H = (m.anchor = h ? h.anchor : c(""));
      let { patchFlag: D, dynamicChildren: B, slotScopeIds: X } = m;
      X && (P = P ? P.concat(X) : X),
        h == null
          ? (o(S, _, b), o(H, _, b), T(m.children, _, H, C, I, $, P, A))
          : D > 0 && D & 64 && B && h.dynamicChildren
          ? (q(h.dynamicChildren, B, _, C, I, $, P),
            (m.key != null || (C && m === C.subTree)) && Hc(h, m, !0))
          : te(h, m, _, H, C, I, $, P, A);
    },
    oe = (h, m, _, b, C, I, $, P, A) => {
      (m.slotScopeIds = P),
        h == null
          ? m.shapeFlag & 512
            ? C.ctx.activate(m, _, b, $, A)
            : de(m, _, b, C, I, $, A)
          : ee(h, m, A);
    },
    de = (h, m, _, b, C, I, $) => {
      const P = (h.component = Pu(h, b, C));
      if ((Co(h) && (P.ctx.renderer = j), Ru(P), P.asyncDep)) {
        if ((C && C.registerDep(P, ce), !h.el)) {
          const A = (P.subTree = J(Ke));
          x(null, A, m, _);
        }
        return;
      }
      ce(P, h, m, _, C, I, $);
    },
    ee = (h, m, _) => {
      const b = (m.component = h.component);
      if (zl(h, m, _))
        if (b.asyncDep && !b.asyncResolved) {
          Q(b, m, _);
          return;
        } else (b.next = m), Ll(b.update), b.update();
      else (m.el = h.el), (b.vnode = m);
    },
    ce = (h, m, _, b, C, I, $) => {
      const P = () => {
          if (h.isMounted) {
            let { next: H, bu: D, u: B, parent: X, vnode: ne } = h,
              he = H,
              fe;
            Rt(h, !1),
              H ? ((H.el = ne.el), Q(h, H, $)) : (H = ne),
              D && Yn(D),
              (fe = H.props && H.props.onVnodeBeforeUpdate) && Ye(fe, X, H, ne),
              Rt(h, !0);
            const ve = Mo(h),
              Be = h.subTree;
            (h.subTree = ve),
              y(Be, ve, f(Be.el), k(Be), h, C, I),
              (H.el = ve.el),
              he === null && Kl(h, ve.el),
              B && Ne(B, C),
              (fe = H.props && H.props.onVnodeUpdated) &&
                Ne(() => Ye(fe, X, H, ne), C);
          } else {
            let H;
            const { el: D, props: B } = m,
              { bm: X, m: ne, parent: he } = h,
              fe = wn(m);
            if (
              (Rt(h, !1),
              X && Yn(X),
              !fe && (H = B && B.onVnodeBeforeMount) && Ye(H, he, m),
              Rt(h, !0),
              D && le)
            ) {
              const ve = () => {
                (h.subTree = Mo(h)), le(D, h.subTree, h, C, null);
              };
              fe
                ? m.type.__asyncLoader().then(() => !h.isUnmounted && ve())
                : ve();
            } else {
              const ve = (h.subTree = Mo(h));
              y(null, ve, _, b, h, C, I), (m.el = ve.el);
            }
            if ((ne && Ne(ne, C), !fe && (H = B && B.onVnodeMounted))) {
              const ve = m;
              Ne(() => Ye(H, he, ve), C);
            }
            (m.shapeFlag & 256 ||
              (he && wn(he.vnode) && he.vnode.shapeFlag & 256)) &&
              h.a &&
              Ne(h.a, C),
              (h.isMounted = !0),
              (m = _ = b = null);
          }
        },
        A = (h.effect = new Ms(P, () => Ws(S), h.scope)),
        S = (h.update = () => A.run());
      (S.id = h.uid), Rt(h, !0), S();
    },
    Q = (h, m, _) => {
      m.component = h;
      const b = h.vnode.props;
      (h.vnode = m),
        (h.next = null),
        gu(h, m.props, b, _),
        vu(h, m.children, _),
        an(),
        Er(),
        ln();
    },
    te = (h, m, _, b, C, I, $, P, A = !1) => {
      const S = h && h.children,
        H = h ? h.shapeFlag : 0,
        D = m.children,
        { patchFlag: B, shapeFlag: X } = m;
      if (B > 0) {
        if (B & 128) {
          Ie(S, D, _, b, C, I, $, P, A);
          return;
        } else if (B & 256) {
          xe(S, D, _, b, C, I, $, P, A);
          return;
        }
      }
      X & 8
        ? (H & 16 && Pe(S, C, I), D !== S && u(_, D))
        : H & 16
        ? X & 16
          ? Ie(S, D, _, b, C, I, $, P, A)
          : Pe(S, C, I, !0)
        : (H & 8 && u(_, ""), X & 16 && T(D, _, b, C, I, $, P, A));
    },
    xe = (h, m, _, b, C, I, $, P, A) => {
      (h = h || Qt), (m = m || Qt);
      const S = h.length,
        H = m.length,
        D = Math.min(S, H);
      let B;
      for (B = 0; B < D; B++) {
        const X = (m[B] = A ? vt(m[B]) : Qe(m[B]));
        y(h[B], X, _, null, C, I, $, P, A);
      }
      S > H ? Pe(h, C, I, !0, !1, D) : T(m, _, b, C, I, $, P, A, D);
    },
    Ie = (h, m, _, b, C, I, $, P, A) => {
      let S = 0;
      const H = m.length;
      let D = h.length - 1,
        B = H - 1;
      for (; S <= D && S <= B; ) {
        const X = h[S],
          ne = (m[S] = A ? vt(m[S]) : Qe(m[S]));
        if (Nt(X, ne)) y(X, ne, _, null, C, I, $, P, A);
        else break;
        S++;
      }
      for (; S <= D && S <= B; ) {
        const X = h[D],
          ne = (m[B] = A ? vt(m[B]) : Qe(m[B]));
        if (Nt(X, ne)) y(X, ne, _, null, C, I, $, P, A);
        else break;
        D--, B--;
      }
      if (S > D) {
        if (S <= B) {
          const X = B + 1,
            ne = X < H ? m[X].el : b;
          for (; S <= B; )
            y(null, (m[S] = A ? vt(m[S]) : Qe(m[S])), _, ne, C, I, $, P, A),
              S++;
        }
      } else if (S > B) for (; S <= D; ) ke(h[S], C, I, !0), S++;
      else {
        const X = S,
          ne = S,
          he = new Map();
        for (S = ne; S <= B; S++) {
          const Fe = (m[S] = A ? vt(m[S]) : Qe(m[S]));
          Fe.key != null && he.set(Fe.key, S);
        }
        let fe,
          ve = 0;
        const Be = B - ne + 1;
        let Vt = !1,
          gr = 0;
        const fn = new Array(Be);
        for (S = 0; S < Be; S++) fn[S] = 0;
        for (S = X; S <= D; S++) {
          const Fe = h[S];
          if (ve >= Be) {
            ke(Fe, C, I, !0);
            continue;
          }
          let Ge;
          if (Fe.key != null) Ge = he.get(Fe.key);
          else
            for (fe = ne; fe <= B; fe++)
              if (fn[fe - ne] === 0 && Nt(Fe, m[fe])) {
                Ge = fe;
                break;
              }
          Ge === void 0
            ? ke(Fe, C, I, !0)
            : ((fn[Ge - ne] = S + 1),
              Ge >= gr ? (gr = Ge) : (Vt = !0),
              y(Fe, m[Ge], _, null, C, I, $, P, A),
              ve++);
        }
        const _r = Vt ? xu(fn) : Qt;
        for (fe = _r.length - 1, S = Be - 1; S >= 0; S--) {
          const Fe = ne + S,
            Ge = m[Fe],
            yr = Fe + 1 < H ? m[Fe + 1].el : b;
          fn[S] === 0
            ? y(null, Ge, _, yr, C, I, $, P, A)
            : Vt && (fe < 0 || S !== _r[fe] ? Ae(Ge, _, yr, 2) : fe--);
        }
      }
    },
    Ae = (h, m, _, b, C = null) => {
      const { el: I, type: $, transition: P, children: A, shapeFlag: S } = h;
      if (S & 6) {
        Ae(h.component.subTree, m, _, b);
        return;
      }
      if (S & 128) {
        h.suspense.move(m, _, b);
        return;
      }
      if (S & 64) {
        $.move(h, m, _, j);
        return;
      }
      if ($ === _e) {
        o(I, m, _);
        for (let D = 0; D < A.length; D++) Ae(A[D], m, _, b);
        o(h.anchor, m, _);
        return;
      }
      if ($ === Uo) {
        O(h, m, _);
        return;
      }
      if (b !== 2 && S & 1 && P)
        if (b === 0) P.beforeEnter(I), o(I, m, _), Ne(() => P.enter(I), C);
        else {
          const { leave: D, delayLeave: B, afterLeave: X } = P,
            ne = () => o(I, m, _),
            he = () => {
              D(I, () => {
                ne(), X && X();
              });
            };
          B ? B(I, ne, he) : he();
        }
      else o(I, m, _);
    },
    ke = (h, m, _, b = !1, C = !1) => {
      const {
        type: I,
        props: $,
        ref: P,
        children: A,
        dynamicChildren: S,
        shapeFlag: H,
        patchFlag: D,
        dirs: B,
      } = h;
      if ((P != null && ps(P, null, _, h, !0), H & 256)) {
        m.ctx.deactivate(h);
        return;
      }
      const X = H & 1 && B,
        ne = !wn(h);
      let he;
      if ((ne && (he = $ && $.onVnodeBeforeUnmount) && Ye(he, m, h), H & 6))
        Tt(h.component, _, b);
      else {
        if (H & 128) {
          h.suspense.unmount(_, b);
          return;
        }
        X && Pt(h, null, m, "beforeUnmount"),
          H & 64
            ? h.type.remove(h, m, _, C, j, b)
            : S && (I !== _e || (D > 0 && D & 64))
            ? Pe(S, m, _, !1, !0)
            : ((I === _e && D & 384) || (!C && H & 16)) && Pe(A, m, _),
          b && it(h);
      }
      ((ne && (he = $ && $.onVnodeUnmounted)) || X) &&
        Ne(() => {
          he && Ye(he, m, h), X && Pt(h, null, m, "unmounted");
        }, _);
    },
    it = (h) => {
      const { type: m, el: _, anchor: b, transition: C } = h;
      if (m === _e) {
        ye(_, b);
        return;
      }
      if (m === Uo) {
        R(h);
        return;
      }
      const I = () => {
        s(_), C && !C.persisted && C.afterLeave && C.afterLeave();
      };
      if (h.shapeFlag & 1 && C && !C.persisted) {
        const { leave: $, delayLeave: P } = C,
          A = () => $(_, I);
        P ? P(h.el, I, A) : A();
      } else I();
    },
    ye = (h, m) => {
      let _;
      for (; h !== m; ) (_ = d(h)), s(h), (h = _);
      s(m);
    },
    Tt = (h, m, _) => {
      const { bum: b, scope: C, update: I, subTree: $, um: P } = h;
      b && Yn(b),
        C.stop(),
        I && ((I.active = !1), ke($, h, m, _)),
        P && Ne(P, m),
        Ne(() => {
          h.isUnmounted = !0;
        }, m),
        m &&
          m.pendingBranch &&
          !m.isUnmounted &&
          h.asyncDep &&
          !h.asyncResolved &&
          h.suspenseId === m.pendingId &&
          (m.deps--, m.deps === 0 && m.resolve());
    },
    Pe = (h, m, _, b = !1, C = !1, I = 0) => {
      for (let $ = I; $ < h.length; $++) ke(h[$], m, _, b, C);
    },
    k = (h) =>
      h.shapeFlag & 6
        ? k(h.component.subTree)
        : h.shapeFlag & 128
        ? h.suspense.next()
        : d(h.anchor || h.el),
    M = (h, m, _) => {
      h == null
        ? m._vnode && ke(m._vnode, null, null, !0)
        : y(m._vnode || null, h, m, null, null, null, _),
        Er(),
        xc(),
        (m._vnode = h);
    },
    j = {
      p: y,
      um: ke,
      m: Ae,
      r: it,
      mt: de,
      mc: T,
      pc: te,
      pbc: q,
      n: k,
      o: e,
    };
  let K, le;
  return t && ([K, le] = t(j)), { render: M, hydrate: K, createApp: pu(M, K) };
}
function Rt({ effect: e, update: t }, n) {
  e.allowRecurse = t.allowRecurse = n;
}
function Hc(e, t, n = !1) {
  const o = e.children,
    s = t.children;
  if (W(o) && W(s))
    for (let r = 0; r < o.length; r++) {
      const i = o[r];
      let c = s[r];
      c.shapeFlag & 1 &&
        !c.dynamicChildren &&
        ((c.patchFlag <= 0 || c.patchFlag === 32) &&
          ((c = s[r] = vt(s[r])), (c.el = i.el)),
        n || Hc(i, c)),
        c.type === So && (c.el = i.el);
    }
}
function xu(e) {
  const t = e.slice(),
    n = [0];
  let o, s, r, i, c;
  const a = e.length;
  for (o = 0; o < a; o++) {
    const l = e[o];
    if (l !== 0) {
      if (((s = n[n.length - 1]), e[s] < l)) {
        (t[o] = s), n.push(o);
        continue;
      }
      for (r = 0, i = n.length - 1; r < i; )
        (c = (r + i) >> 1), e[n[c]] < l ? (r = c + 1) : (i = c);
      l < e[n[r]] && (r > 0 && (t[o] = n[r - 1]), (n[r] = o));
    }
  }
  for (r = n.length, i = n[r - 1]; r-- > 0; ) (n[r] = i), (i = t[i]);
  return n;
}
const ku = (e) => e.__isTeleport,
  _e = Symbol.for("v-fgt"),
  So = Symbol.for("v-txt"),
  Ke = Symbol.for("v-cmt"),
  Uo = Symbol.for("v-stc"),
  kn = [];
let Ze = null;
function V(e = !1) {
  kn.push((Ze = e ? null : []));
}
function Cu() {
  kn.pop(), (Ze = kn[kn.length - 1] || null);
}
let jn = 1;
function Dr(e) {
  jn += e;
}
function Bc(e) {
  return (
    (e.dynamicChildren = jn > 0 ? Ze || Qt : null),
    Cu(),
    jn > 0 && Ze && Ze.push(e),
    e
  );
}
function G(e, t, n, o, s, r) {
  return Bc(E(e, t, n, o, s, r, !0));
}
function Wt(e, t, n, o, s) {
  return Bc(J(e, t, n, o, s, !0));
}
function ho(e) {
  return e ? e.__v_isVNode === !0 : !1;
}
function Nt(e, t) {
  return e.type === t.type && e.key === t.key;
}
const Eo = "__vInternal",
  Wc = ({ key: e }) => e ?? null,
  to = ({ ref: e, ref_key: t, ref_for: n }) => (
    typeof e == "number" && (e = "" + e),
    e != null
      ? we(e) || ge(e) || Y(e)
        ? { i: Te, r: e, k: t, f: !!n }
        : e
      : null
  );
function E(
  e,
  t = null,
  n = null,
  o = 0,
  s = null,
  r = e === _e ? 0 : 1,
  i = !1,
  c = !1
) {
  const a = {
    __v_isVNode: !0,
    __v_skip: !0,
    type: e,
    props: t,
    key: t && Wc(t),
    ref: t && to(t),
    scopeId: Ic,
    slotScopeIds: null,
    children: n,
    component: null,
    suspense: null,
    ssContent: null,
    ssFallback: null,
    dirs: null,
    transition: null,
    el: null,
    anchor: null,
    target: null,
    targetAnchor: null,
    staticCount: 0,
    shapeFlag: r,
    patchFlag: o,
    dynamicProps: s,
    dynamicChildren: null,
    appContext: null,
    ctx: Te,
  };
  return (
    c
      ? (Js(a, n), r & 128 && e.normalize(a))
      : n && (a.shapeFlag |= we(n) ? 8 : 16),
    jn > 0 &&
      !i &&
      Ze &&
      (a.patchFlag > 0 || r & 6) &&
      a.patchFlag !== 32 &&
      Ze.push(a),
    a
  );
}
const J = Iu;
function Iu(e, t = null, n = null, o = 0, s = null, r = !1) {
  if (((!e || e === ru) && (e = Ke), ho(e))) {
    const c = St(e, t, !0);
    return (
      n && Js(c, n),
      jn > 0 &&
        !r &&
        Ze &&
        (c.shapeFlag & 6 ? (Ze[Ze.indexOf(e)] = c) : Ze.push(c)),
      (c.patchFlag |= -2),
      c
    );
  }
  if ((Nu(e) && (e = e.__vccOpts), t)) {
    t = Su(t);
    let { class: c, style: a } = t;
    c && !we(c) && (t.class = Kt(c)),
      me(a) && (mc(a) && !W(a) && (a = be({}, a)), (t.style = bo(a)));
  }
  const i = we(e) ? 1 : Hl(e) ? 128 : ku(e) ? 64 : me(e) ? 4 : Y(e) ? 2 : 0;
  return E(e, t, n, o, s, i, r, !0);
}
function Su(e) {
  return e ? (mc(e) || Eo in e ? be({}, e) : e) : null;
}
function St(e, t, n = !1) {
  const { props: o, ref: s, patchFlag: r, children: i } = e,
    c = t ? Eu(o || {}, t) : o;
  return {
    __v_isVNode: !0,
    __v_skip: !0,
    type: e.type,
    props: c,
    key: c && Wc(c),
    ref:
      t && t.ref ? (n && s ? (W(s) ? s.concat(to(t)) : [s, to(t)]) : to(t)) : s,
    scopeId: e.scopeId,
    slotScopeIds: e.slotScopeIds,
    children: i,
    target: e.target,
    targetAnchor: e.targetAnchor,
    staticCount: e.staticCount,
    shapeFlag: e.shapeFlag,
    patchFlag: t && e.type !== _e ? (r === -1 ? 16 : r | 16) : r,
    dynamicProps: e.dynamicProps,
    dynamicChildren: e.dynamicChildren,
    appContext: e.appContext,
    dirs: e.dirs,
    transition: e.transition,
    component: e.component,
    suspense: e.suspense,
    ssContent: e.ssContent && St(e.ssContent),
    ssFallback: e.ssFallback && St(e.ssFallback),
    el: e.el,
    anchor: e.anchor,
    ctx: e.ctx,
    ce: e.ce,
  };
}
function Et(e = " ", t = 0) {
  return J(So, null, e, t);
}
function un(e = "", t = !1) {
  return t ? (V(), Wt(Ke, null, e)) : J(Ke, null, e);
}
function Qe(e) {
  return e == null || typeof e == "boolean"
    ? J(Ke)
    : W(e)
    ? J(_e, null, e.slice())
    : typeof e == "object"
    ? vt(e)
    : J(So, null, String(e));
}
function vt(e) {
  return (e.el === null && e.patchFlag !== -1) || e.memo ? e : St(e);
}
function Js(e, t) {
  let n = 0;
  const { shapeFlag: o } = e;
  if (t == null) t = null;
  else if (W(t)) n = 16;
  else if (typeof t == "object")
    if (o & 65) {
      const s = t.default;
      s && (s._c && (s._d = !1), Js(e, s()), s._c && (s._d = !0));
      return;
    } else {
      n = 32;
      const s = t._;
      !s && !(Eo in t)
        ? (t._ctx = Te)
        : s === 3 &&
          Te &&
          (Te.slots._ === 1 ? (t._ = 1) : ((t._ = 2), (e.patchFlag |= 1024)));
    }
  else
    Y(t)
      ? ((t = { default: t, _ctx: Te }), (n = 32))
      : ((t = String(t)), o & 64 ? ((n = 16), (t = [Et(t)])) : (n = 8));
  (e.children = t), (e.shapeFlag |= n);
}
function Eu(...e) {
  const t = {};
  for (let n = 0; n < e.length; n++) {
    const o = e[n];
    for (const s in o)
      if (s === "class")
        t.class !== o.class && (t.class = Kt([t.class, o.class]));
      else if (s === "style") t.style = bo([t.style, o.style]);
      else if (go(s)) {
        const r = t[s],
          i = o[s];
        i &&
          r !== i &&
          !(W(r) && r.includes(i)) &&
          (t[s] = r ? [].concat(r, i) : i);
      } else s !== "" && (t[s] = o[s]);
  }
  return t;
}
function Ye(e, t, n, o = null) {
  ze(e, t, 7, [n, o]);
}
const Ou = Mc();
let Tu = 0;
function Pu(e, t, n) {
  const o = e.type,
    s = (t ? t.appContext : e.appContext) || Ou,
    r = {
      uid: Tu++,
      vnode: e,
      type: o,
      parent: t,
      appContext: s,
      root: null,
      next: null,
      subTree: null,
      effect: null,
      update: null,
      scope: new nc(!0),
      render: null,
      proxy: null,
      exposed: null,
      exposeProxy: null,
      withProxy: null,
      provides: t ? t.provides : Object.create(s.provides),
      accessCache: null,
      renderCache: [],
      components: null,
      directives: null,
      propsOptions: Dc(o, s),
      emitsOptions: Cc(o, s),
      emit: null,
      emitted: null,
      propsDefaults: pe,
      inheritAttrs: o.inheritAttrs,
      ctx: pe,
      data: pe,
      props: pe,
      attrs: pe,
      slots: pe,
      refs: pe,
      setupState: pe,
      setupContext: null,
      attrsProxy: null,
      slotsProxy: null,
      suspense: n,
      suspenseId: n ? n.pendingId : 0,
      asyncDep: null,
      asyncResolved: !1,
      isMounted: !1,
      isUnmounted: !1,
      isDeactivated: !1,
      bc: null,
      c: null,
      bm: null,
      m: null,
      bu: null,
      u: null,
      um: null,
      bum: null,
      da: null,
      a: null,
      rtg: null,
      rtc: null,
      ec: null,
      sp: null,
    };
  return (
    (r.ctx = { _: r }),
    (r.root = t ? t.root : r),
    (r.emit = Fl.bind(null, r)),
    e.ce && e.ce(r),
    r
  );
}
let Se = null;
const Vc = () => Se || Te;
let Gs,
  Zt,
  Ur = "__VUE_INSTANCE_SETTERS__";
(Zt = os()[Ur]) || (Zt = os()[Ur] = []),
  Zt.push((e) => (Se = e)),
  (Gs = (e) => {
    Zt.length > 1 ? Zt.forEach((t) => t(e)) : Zt[0](e);
  });
const sn = (e) => {
    Gs(e), e.scope.on();
  },
  zt = () => {
    Se && Se.scope.off(), Gs(null);
  };
function Zc(e) {
  return e.vnode.shapeFlag & 4;
}
let $n = !1;
function Ru(e, t = !1) {
  $n = t;
  const { props: n, children: o } = e.vnode,
    s = Zc(e);
  mu(e, n, s, t), yu(e, o);
  const r = s ? Au(e, t) : void 0;
  return ($n = !1), r;
}
function Au(e, t) {
  const n = e.type;
  (e.accessCache = Object.create(null)), (e.proxy = on(new Proxy(e.ctx, cu)));
  const { setup: o } = n;
  if (o) {
    const s = (e.setupContext = o.length > 1 ? $u(e) : null);
    sn(e), an();
    const r = kt(o, e, 0, [e.props, s]);
    if ((ln(), zt(), Gi(r))) {
      if ((r.then(zt, zt), t))
        return r
          .then((i) => {
            zr(e, i, t);
          })
          .catch((i) => {
            xo(i, e, 0);
          });
      e.asyncDep = r;
    } else zr(e, r, t);
  } else qc(e, t);
}
function zr(e, t, n) {
  Y(t)
    ? e.type.__ssrInlineRender
      ? (e.ssrRender = t)
      : (e.render = t)
    : me(t) && (e.setupState = vc(t)),
    qc(e, n);
}
let Kr;
function qc(e, t, n) {
  const o = e.type;
  if (!e.render) {
    if (!t && Kr && !o.render) {
      const s = o.template || qs(e).template;
      if (s) {
        const { isCustomElement: r, compilerOptions: i } = e.appContext.config,
          { delimiters: c, compilerOptions: a } = o,
          l = be(be({ isCustomElement: r, delimiters: c }, i), a);
        o.render = Kr(s, l);
      }
    }
    e.render = o.render || qe;
  }
  sn(e), an(), au(e), ln(), zt();
}
function ju(e) {
  return (
    e.attrsProxy ||
    (e.attrsProxy = new Proxy(e.attrs, {
      get(t, n) {
        return Me(e, "get", "$attrs"), t[n];
      },
    }))
  );
}
function $u(e) {
  const t = (n) => {
    e.exposed = n || {};
  };
  return {
    get attrs() {
      return ju(e);
    },
    slots: e.slots,
    emit: e.emit,
    expose: t,
  };
}
function Oo(e) {
  if (e.exposed)
    return (
      e.exposeProxy ||
      (e.exposeProxy = new Proxy(vc(on(e.exposed)), {
        get(t, n) {
          if (n in t) return t[n];
          if (n in xn) return xn[n](e);
        },
        has(t, n) {
          return n in t || n in xn;
        },
      }))
    );
}
function Lu(e, t = !0) {
  return Y(e) ? e.displayName || e.name : e.name || (t && e.__name);
}
function Nu(e) {
  return Y(e) && "__vccOpts" in e;
}
const Oe = (e, t) => Al(e, t, $n);
function Ln(e, t, n) {
  const o = arguments.length;
  return o === 2
    ? me(t) && !W(t)
      ? ho(t)
        ? J(e, null, [t])
        : J(e, t)
      : J(e, null, t)
    : (o > 3
        ? (n = Array.prototype.slice.call(arguments, 2))
        : o === 3 && ho(n) && (n = [n]),
      J(e, t, n));
}
const Mu = Symbol.for("v-scx"),
  Fu = () => Xe(Mu),
  Du = "3.3.2",
  Uu = "http://www.w3.org/2000/svg",
  Mt = typeof document < "u" ? document : null,
  Hr = Mt && Mt.createElement("template"),
  zu = {
    insert: (e, t, n) => {
      t.insertBefore(e, n || null);
    },
    remove: (e) => {
      const t = e.parentNode;
      t && t.removeChild(e);
    },
    createElement: (e, t, n, o) => {
      const s = t
        ? Mt.createElementNS(Uu, e)
        : Mt.createElement(e, n ? { is: n } : void 0);
      return (
        e === "select" &&
          o &&
          o.multiple != null &&
          s.setAttribute("multiple", o.multiple),
        s
      );
    },
    createText: (e) => Mt.createTextNode(e),
    createComment: (e) => Mt.createComment(e),
    setText: (e, t) => {
      e.nodeValue = t;
    },
    setElementText: (e, t) => {
      e.textContent = t;
    },
    parentNode: (e) => e.parentNode,
    nextSibling: (e) => e.nextSibling,
    querySelector: (e) => Mt.querySelector(e),
    setScopeId(e, t) {
      e.setAttribute(t, "");
    },
    insertStaticContent(e, t, n, o, s, r) {
      const i = n ? n.previousSibling : t.lastChild;
      if (s && (s === r || s.nextSibling))
        for (
          ;
          t.insertBefore(s.cloneNode(!0), n),
            !(s === r || !(s = s.nextSibling));

        );
      else {
        Hr.innerHTML = o ? `<svg>${e}</svg>` : e;
        const c = Hr.content;
        if (o) {
          const a = c.firstChild;
          for (; a.firstChild; ) c.appendChild(a.firstChild);
          c.removeChild(a);
        }
        t.insertBefore(c, n);
      }
      return [
        i ? i.nextSibling : t.firstChild,
        n ? n.previousSibling : t.lastChild,
      ];
    },
  };
function Ku(e, t, n) {
  const o = e._vtc;
  o && (t = (t ? [t, ...o] : [...o]).join(" ")),
    t == null
      ? e.removeAttribute("class")
      : n
      ? e.setAttribute("class", t)
      : (e.className = t);
}
function Hu(e, t, n) {
  const o = e.style,
    s = we(n);
  if (n && !s) {
    if (t && !we(t)) for (const r in t) n[r] == null && ms(o, r, "");
    for (const r in n) ms(o, r, n[r]);
  } else {
    const r = o.display;
    s ? t !== n && (o.cssText = n) : t && e.removeAttribute("style"),
      "_vod" in e && (o.display = r);
  }
}
const Br = /\s*!important$/;
function ms(e, t, n) {
  if (W(n)) n.forEach((o) => ms(e, t, o));
  else if ((n == null && (n = ""), t.startsWith("--"))) e.setProperty(t, n);
  else {
    const o = Bu(e, t);
    Br.test(n)
      ? e.setProperty(Bt(o), n.replace(Br, ""), "important")
      : (e[o] = n);
  }
}
const Wr = ["Webkit", "Moz", "ms"],
  zo = {};
function Bu(e, t) {
  const n = zo[t];
  if (n) return n;
  let o = ot(t);
  if (o !== "filter" && o in e) return (zo[t] = o);
  o = vo(o);
  for (let s = 0; s < Wr.length; s++) {
    const r = Wr[s] + o;
    if (r in e) return (zo[t] = r);
  }
  return t;
}
const Vr = "http://www.w3.org/1999/xlink";
function Wu(e, t, n, o, s) {
  if (o && t.startsWith("xlink:"))
    n == null
      ? e.removeAttributeNS(Vr, t.slice(6, t.length))
      : e.setAttributeNS(Vr, t, n);
  else {
    const r = Ja(t);
    n == null || (r && !ec(n))
      ? e.removeAttribute(t)
      : e.setAttribute(t, r ? "" : n);
  }
}
function Vu(e, t, n, o, s, r, i) {
  if (t === "innerHTML" || t === "textContent") {
    o && i(o, s, r), (e[t] = n ?? "");
    return;
  }
  const c = e.tagName;
  if (t === "value" && c !== "PROGRESS" && !c.includes("-")) {
    e._value = n;
    const l = c === "OPTION" ? e.getAttribute("value") : e.value,
      u = n ?? "";
    l !== u && (e.value = u), n == null && e.removeAttribute(t);
    return;
  }
  let a = !1;
  if (n === "" || n == null) {
    const l = typeof e[t];
    l === "boolean"
      ? (n = ec(n))
      : n == null && l === "string"
      ? ((n = ""), (a = !0))
      : l === "number" && ((n = 0), (a = !0));
  }
  try {
    e[t] = n;
  } catch {}
  a && e.removeAttribute(t);
}
function Xt(e, t, n, o) {
  e.addEventListener(t, n, o);
}
function Zu(e, t, n, o) {
  e.removeEventListener(t, n, o);
}
function qu(e, t, n, o, s = null) {
  const r = e._vei || (e._vei = {}),
    i = r[t];
  if (o && i) i.value = o;
  else {
    const [c, a] = Xu(t);
    if (o) {
      const l = (r[t] = Yu(o, s));
      Xt(e, c, l, a);
    } else i && (Zu(e, c, i, a), (r[t] = void 0));
  }
}
const Zr = /(?:Once|Passive|Capture)$/;
function Xu(e) {
  let t;
  if (Zr.test(e)) {
    t = {};
    let o;
    for (; (o = e.match(Zr)); )
      (e = e.slice(0, e.length - o[0].length)), (t[o[0].toLowerCase()] = !0);
  }
  return [e[2] === ":" ? e.slice(3) : Bt(e.slice(2)), t];
}
let Ko = 0;
const Ju = Promise.resolve(),
  Gu = () => Ko || (Ju.then(() => (Ko = 0)), (Ko = Date.now()));
function Yu(e, t) {
  const n = (o) => {
    if (!o._vts) o._vts = Date.now();
    else if (o._vts <= n.attached) return;
    ze(Qu(o, n.value), t, 5, [o]);
  };
  return (n.value = e), (n.attached = Gu()), n;
}
function Qu(e, t) {
  if (W(t)) {
    const n = e.stopImmediatePropagation;
    return (
      (e.stopImmediatePropagation = () => {
        n.call(e), (e._stopped = !0);
      }),
      t.map((o) => (s) => !s._stopped && o && o(s))
    );
  } else return t;
}
const qr = /^on[a-z]/,
  ef = (e, t, n, o, s = !1, r, i, c, a) => {
    t === "class"
      ? Ku(e, o, s)
      : t === "style"
      ? Hu(e, n, o)
      : go(t)
      ? Rs(t) || qu(e, t, n, o, i)
      : (
          t[0] === "."
            ? ((t = t.slice(1)), !0)
            : t[0] === "^"
            ? ((t = t.slice(1)), !1)
            : tf(e, t, o, s)
        )
      ? Vu(e, t, o, r, i, c, a)
      : (t === "true-value"
          ? (e._trueValue = o)
          : t === "false-value" && (e._falseValue = o),
        Wu(e, t, o, s));
  };
function tf(e, t, n, o) {
  return o
    ? !!(
        t === "innerHTML" ||
        t === "textContent" ||
        (t in e && qr.test(t) && Y(n))
      )
    : t === "spellcheck" ||
      t === "draggable" ||
      t === "translate" ||
      t === "form" ||
      (t === "list" && e.tagName === "INPUT") ||
      (t === "type" && e.tagName === "TEXTAREA") ||
      (qr.test(t) && we(n))
    ? !1
    : t in e;
}
const mt = "transition",
  dn = "animation",
  Ys = (e, { slots: t }) => Ln(ql, nf(e), t);
Ys.displayName = "Transition";
const Xc = {
  name: String,
  type: String,
  css: { type: Boolean, default: !0 },
  duration: [String, Number, Object],
  enterFromClass: String,
  enterActiveClass: String,
  enterToClass: String,
  appearFromClass: String,
  appearActiveClass: String,
  appearToClass: String,
  leaveFromClass: String,
  leaveActiveClass: String,
  leaveToClass: String,
};
Ys.props = be({}, Tc, Xc);
const At = (e, t = []) => {
    W(e) ? e.forEach((n) => n(...t)) : e && e(...t);
  },
  Xr = (e) => (e ? (W(e) ? e.some((t) => t.length > 1) : e.length > 1) : !1);
function nf(e) {
  const t = {};
  for (const L in e) L in Xc || (t[L] = e[L]);
  if (e.css === !1) return t;
  const {
      name: n = "v",
      type: o,
      duration: s,
      enterFromClass: r = `${n}-enter-from`,
      enterActiveClass: i = `${n}-enter-active`,
      enterToClass: c = `${n}-enter-to`,
      appearFromClass: a = r,
      appearActiveClass: l = i,
      appearToClass: u = c,
      leaveFromClass: f = `${n}-leave-from`,
      leaveActiveClass: d = `${n}-leave-active`,
      leaveToClass: p = `${n}-leave-to`,
    } = e,
    g = of(s),
    y = g && g[0],
    w = g && g[1],
    {
      onBeforeEnter: x,
      onEnter: v,
      onEnterCancelled: O,
      onLeave: R,
      onLeaveCancelled: U,
      onBeforeAppear: F = x,
      onAppear: N = v,
      onAppearCancelled: T = O,
    } = t,
    Z = (L, oe, de) => {
      jt(L, oe ? u : c), jt(L, oe ? l : i), de && de();
    },
    q = (L, oe) => {
      (L._isLeaving = !1), jt(L, f), jt(L, p), jt(L, d), oe && oe();
    },
    ae = (L) => (oe, de) => {
      const ee = L ? N : v,
        ce = () => Z(oe, L, de);
      At(ee, [oe, ce]),
        Jr(() => {
          jt(oe, L ? a : r), gt(oe, L ? u : c), Xr(ee) || Gr(oe, o, y, ce);
        });
    };
  return be(t, {
    onBeforeEnter(L) {
      At(x, [L]), gt(L, r), gt(L, i);
    },
    onBeforeAppear(L) {
      At(F, [L]), gt(L, a), gt(L, l);
    },
    onEnter: ae(!1),
    onAppear: ae(!0),
    onLeave(L, oe) {
      L._isLeaving = !0;
      const de = () => q(L, oe);
      gt(L, f),
        cf(),
        gt(L, d),
        Jr(() => {
          L._isLeaving && (jt(L, f), gt(L, p), Xr(R) || Gr(L, o, w, de));
        }),
        At(R, [L, de]);
    },
    onEnterCancelled(L) {
      Z(L, !1), At(O, [L]);
    },
    onAppearCancelled(L) {
      Z(L, !0), At(T, [L]);
    },
    onLeaveCancelled(L) {
      q(L), At(U, [L]);
    },
  });
}
function of(e) {
  if (e == null) return null;
  if (me(e)) return [Ho(e.enter), Ho(e.leave)];
  {
    const t = Ho(e);
    return [t, t];
  }
}
function Ho(e) {
  return Ba(e);
}
function gt(e, t) {
  t.split(/\s+/).forEach((n) => n && e.classList.add(n)),
    (e._vtc || (e._vtc = new Set())).add(t);
}
function jt(e, t) {
  t.split(/\s+/).forEach((o) => o && e.classList.remove(o));
  const { _vtc: n } = e;
  n && (n.delete(t), n.size || (e._vtc = void 0));
}
function Jr(e) {
  requestAnimationFrame(() => {
    requestAnimationFrame(e);
  });
}
let sf = 0;
function Gr(e, t, n, o) {
  const s = (e._endId = ++sf),
    r = () => {
      s === e._endId && o();
    };
  if (n) return setTimeout(r, n);
  const { type: i, timeout: c, propCount: a } = rf(e, t);
  if (!i) return o();
  const l = i + "end";
  let u = 0;
  const f = () => {
      e.removeEventListener(l, d), r();
    },
    d = (p) => {
      p.target === e && ++u >= a && f();
    };
  setTimeout(() => {
    u < a && f();
  }, c + 1),
    e.addEventListener(l, d);
}
function rf(e, t) {
  const n = window.getComputedStyle(e),
    o = (g) => (n[g] || "").split(", "),
    s = o(`${mt}Delay`),
    r = o(`${mt}Duration`),
    i = Yr(s, r),
    c = o(`${dn}Delay`),
    a = o(`${dn}Duration`),
    l = Yr(c, a);
  let u = null,
    f = 0,
    d = 0;
  t === mt
    ? i > 0 && ((u = mt), (f = i), (d = r.length))
    : t === dn
    ? l > 0 && ((u = dn), (f = l), (d = a.length))
    : ((f = Math.max(i, l)),
      (u = f > 0 ? (i > l ? mt : dn) : null),
      (d = u ? (u === mt ? r.length : a.length) : 0));
  const p =
    u === mt && /\b(transform|all)(,|$)/.test(o(`${mt}Property`).toString());
  return { type: u, timeout: f, propCount: d, hasTransform: p };
}
function Yr(e, t) {
  for (; e.length < t.length; ) e = e.concat(e);
  return Math.max(...t.map((n, o) => Qr(n) + Qr(e[o])));
}
function Qr(e) {
  return Number(e.slice(0, -1).replace(",", ".")) * 1e3;
}
function cf() {
  return document.body.offsetHeight;
}
const ei = (e) => {
  const t = e.props["onUpdate:modelValue"] || !1;
  return W(t) ? (n) => Yn(t, n) : t;
};
function af(e) {
  e.target.composing = !0;
}
function ti(e) {
  const t = e.target;
  t.composing && ((t.composing = !1), t.dispatchEvent(new Event("input")));
}
const Jc = {
    created(e, { modifiers: { lazy: t, trim: n, number: o } }, s) {
      e._assign = ei(s);
      const r = o || (s.props && s.props.type === "number");
      Xt(e, t ? "change" : "input", (i) => {
        if (i.target.composing) return;
        let c = e.value;
        n && (c = c.trim()), r && (c = ns(c)), e._assign(c);
      }),
        n &&
          Xt(e, "change", () => {
            e.value = e.value.trim();
          }),
        t ||
          (Xt(e, "compositionstart", af),
          Xt(e, "compositionend", ti),
          Xt(e, "change", ti));
    },
    mounted(e, { value: t }) {
      e.value = t ?? "";
    },
    beforeUpdate(
      e,
      { value: t, modifiers: { lazy: n, trim: o, number: s } },
      r
    ) {
      if (
        ((e._assign = ei(r)),
        e.composing ||
          (document.activeElement === e &&
            e.type !== "range" &&
            (n ||
              (o && e.value.trim() === t) ||
              ((s || e.type === "number") && ns(e.value) === t))))
      )
        return;
      const i = t ?? "";
      e.value !== i && (e.value = i);
    },
  },
  lf = ["ctrl", "shift", "alt", "meta"],
  uf = {
    stop: (e) => e.stopPropagation(),
    prevent: (e) => e.preventDefault(),
    self: (e) => e.target !== e.currentTarget,
    ctrl: (e) => !e.ctrlKey,
    shift: (e) => !e.shiftKey,
    alt: (e) => !e.altKey,
    meta: (e) => !e.metaKey,
    left: (e) => "button" in e && e.button !== 0,
    middle: (e) => "button" in e && e.button !== 1,
    right: (e) => "button" in e && e.button !== 2,
    exact: (e, t) => lf.some((n) => e[`${n}Key`] && !t.includes(n)),
  },
  Gc =
    (e, t) =>
    (n, ...o) => {
      for (let s = 0; s < t.length; s++) {
        const r = uf[t[s]];
        if (r && r(n, t)) return;
      }
      return e(n, ...o);
    },
  ff = {
    esc: "escape",
    space: " ",
    up: "arrow-up",
    left: "arrow-left",
    right: "arrow-right",
    down: "arrow-down",
    delete: "backspace",
  },
  df = (e, t) => (n) => {
    if (!("key" in n)) return;
    const o = Bt(n.key);
    if (t.some((s) => s === o || ff[s] === o)) return e(n);
  },
  hf = be({ patchProp: ef }, zu);
let ni;
function pf() {
  return ni || (ni = bu(hf));
}
const mf = (...e) => {
  const t = pf().createApp(...e),
    { mount: n } = t;
  return (
    (t.mount = (o) => {
      const s = gf(o);
      if (!s) return;
      const r = t._component;
      !Y(r) && !r.render && !r.template && (r.template = s.innerHTML),
        (s.innerHTML = "");
      const i = n(s, !1, s instanceof SVGElement);
      return (
        s instanceof Element &&
          (s.removeAttribute("v-cloak"), s.setAttribute("data-v-app", "")),
        i
      );
    }),
    t
  );
};
function gf(e) {
  return we(e) ? document.querySelector(e) : e;
}
/*!
 * vue-router v4.2.0
 * (c) 2023 Eduardo San Martin Morote
 * @license MIT
 */ const Jt = typeof window < "u";
function _f(e) {
  return e.__esModule || e[Symbol.toStringTag] === "Module";
}
const ue = Object.assign;
function Bo(e, t) {
  const n = {};
  for (const o in t) {
    const s = t[o];
    n[o] = Je(s) ? s.map(e) : e(s);
  }
  return n;
}
const Cn = () => {},
  Je = Array.isArray,
  yf = /\/$/,
  vf = (e) => e.replace(yf, "");
function Wo(e, t, n = "/") {
  let o,
    s = {},
    r = "",
    i = "";
  const c = t.indexOf("#");
  let a = t.indexOf("?");
  return (
    c < a && c >= 0 && (a = -1),
    a > -1 &&
      ((o = t.slice(0, a)),
      (r = t.slice(a + 1, c > -1 ? c : t.length)),
      (s = e(r))),
    c > -1 && ((o = o || t.slice(0, c)), (i = t.slice(c, t.length))),
    (o = kf(o ?? t, n)),
    { fullPath: o + (r && "?") + r + i, path: o, query: s, hash: i }
  );
}
function bf(e, t) {
  const n = t.query ? e(t.query) : "";
  return t.path + (n && "?") + n + (t.hash || "");
}
function oi(e, t) {
  return !t || !e.toLowerCase().startsWith(t.toLowerCase())
    ? e
    : e.slice(t.length) || "/";
}
function wf(e, t, n) {
  const o = t.matched.length - 1,
    s = n.matched.length - 1;
  return (
    o > -1 &&
    o === s &&
    rn(t.matched[o], n.matched[s]) &&
    Yc(t.params, n.params) &&
    e(t.query) === e(n.query) &&
    t.hash === n.hash
  );
}
function rn(e, t) {
  return (e.aliasOf || e) === (t.aliasOf || t);
}
function Yc(e, t) {
  if (Object.keys(e).length !== Object.keys(t).length) return !1;
  for (const n in e) if (!xf(e[n], t[n])) return !1;
  return !0;
}
function xf(e, t) {
  return Je(e) ? si(e, t) : Je(t) ? si(t, e) : e === t;
}
function si(e, t) {
  return Je(t)
    ? e.length === t.length && e.every((n, o) => n === t[o])
    : e.length === 1 && e[0] === t;
}
function kf(e, t) {
  if (e.startsWith("/")) return e;
  if (!e) return t;
  const n = t.split("/"),
    o = e.split("/"),
    s = o[o.length - 1];
  (s === ".." || s === ".") && o.push("");
  let r = n.length - 1,
    i,
    c;
  for (i = 0; i < o.length; i++)
    if (((c = o[i]), c !== "."))
      if (c === "..") r > 1 && r--;
      else break;
  return (
    n.slice(0, r).join("/") +
    "/" +
    o.slice(i - (i === o.length ? 1 : 0)).join("/")
  );
}
var Nn;
(function (e) {
  (e.pop = "pop"), (e.push = "push");
})(Nn || (Nn = {}));
var In;
(function (e) {
  (e.back = "back"), (e.forward = "forward"), (e.unknown = "");
})(In || (In = {}));
function Cf(e) {
  if (!e)
    if (Jt) {
      const t = document.querySelector("base");
      (e = (t && t.getAttribute("href")) || "/"),
        (e = e.replace(/^\w+:\/\/[^\/]+/, ""));
    } else e = "/";
  return e[0] !== "/" && e[0] !== "#" && (e = "/" + e), vf(e);
}
const If = /^[^#]+#/;
function Sf(e, t) {
  return e.replace(If, "#") + t;
}
function Ef(e, t) {
  const n = document.documentElement.getBoundingClientRect(),
    o = e.getBoundingClientRect();
  return {
    behavior: t.behavior,
    left: o.left - n.left - (t.left || 0),
    top: o.top - n.top - (t.top || 0),
  };
}
const To = () => ({ left: window.pageXOffset, top: window.pageYOffset });
function Of(e) {
  let t;
  if ("el" in e) {
    const n = e.el,
      o = typeof n == "string" && n.startsWith("#"),
      s =
        typeof n == "string"
          ? o
            ? document.getElementById(n.slice(1))
            : document.querySelector(n)
          : n;
    if (!s) return;
    t = Ef(s, e);
  } else t = e;
  "scrollBehavior" in document.documentElement.style
    ? window.scrollTo(t)
    : window.scrollTo(
        t.left != null ? t.left : window.pageXOffset,
        t.top != null ? t.top : window.pageYOffset
      );
}
function ri(e, t) {
  return (history.state ? history.state.position - t : -1) + e;
}
const gs = new Map();
function Tf(e, t) {
  gs.set(e, t);
}
function Pf(e) {
  const t = gs.get(e);
  return gs.delete(e), t;
}
let Rf = () => location.protocol + "//" + location.host;
function Qc(e, t) {
  const { pathname: n, search: o, hash: s } = t,
    r = e.indexOf("#");
  if (r > -1) {
    let c = s.includes(e.slice(r)) ? e.slice(r).length : 1,
      a = s.slice(c);
    return a[0] !== "/" && (a = "/" + a), oi(a, "");
  }
  return oi(n, e) + o + s;
}
function Af(e, t, n, o) {
  let s = [],
    r = [],
    i = null;
  const c = ({ state: d }) => {
    const p = Qc(e, location),
      g = n.value,
      y = t.value;
    let w = 0;
    if (d) {
      if (((n.value = p), (t.value = d), i && i === g)) {
        i = null;
        return;
      }
      w = y ? d.position - y.position : 0;
    } else o(p);
    s.forEach((x) => {
      x(n.value, g, {
        delta: w,
        type: Nn.pop,
        direction: w ? (w > 0 ? In.forward : In.back) : In.unknown,
      });
    });
  };
  function a() {
    i = n.value;
  }
  function l(d) {
    s.push(d);
    const p = () => {
      const g = s.indexOf(d);
      g > -1 && s.splice(g, 1);
    };
    return r.push(p), p;
  }
  function u() {
    const { history: d } = window;
    d.state && d.replaceState(ue({}, d.state, { scroll: To() }), "");
  }
  function f() {
    for (const d of r) d();
    (r = []),
      window.removeEventListener("popstate", c),
      window.removeEventListener("beforeunload", u);
  }
  return (
    window.addEventListener("popstate", c),
    window.addEventListener("beforeunload", u, { passive: !0 }),
    { pauseListeners: a, listen: l, destroy: f }
  );
}
function ii(e, t, n, o = !1, s = !1) {
  return {
    back: e,
    current: t,
    forward: n,
    replaced: o,
    position: window.history.length,
    scroll: s ? To() : null,
  };
}
function jf(e) {
  const { history: t, location: n } = window,
    o = { value: Qc(e, n) },
    s = { value: t.state };
  s.value ||
    r(
      o.value,
      {
        back: null,
        current: o.value,
        forward: null,
        position: t.length - 1,
        replaced: !0,
        scroll: null,
      },
      !0
    );
  function r(a, l, u) {
    const f = e.indexOf("#"),
      d =
        f > -1
          ? (n.host && document.querySelector("base") ? e : e.slice(f)) + a
          : Rf() + e + a;
    try {
      t[u ? "replaceState" : "pushState"](l, "", d), (s.value = l);
    } catch (p) {
      console.error(p), n[u ? "replace" : "assign"](d);
    }
  }
  function i(a, l) {
    const u = ue({}, t.state, ii(s.value.back, a, s.value.forward, !0), l, {
      position: s.value.position,
    });
    r(a, u, !0), (o.value = a);
  }
  function c(a, l) {
    const u = ue({}, s.value, t.state, { forward: a, scroll: To() });
    r(u.current, u, !0);
    const f = ue({}, ii(o.value, a, null), { position: u.position + 1 }, l);
    r(a, f, !1), (o.value = a);
  }
  return { location: o, state: s, push: c, replace: i };
}
function $f(e) {
  e = Cf(e);
  const t = jf(e),
    n = Af(e, t.state, t.location, t.replace);
  function o(r, i = !0) {
    i || n.pauseListeners(), history.go(r);
  }
  const s = ue(
    { location: "", base: e, go: o, createHref: Sf.bind(null, e) },
    t,
    n
  );
  return (
    Object.defineProperty(s, "location", {
      enumerable: !0,
      get: () => t.location.value,
    }),
    Object.defineProperty(s, "state", {
      enumerable: !0,
      get: () => t.state.value,
    }),
    s
  );
}
function Lf(e) {
  return typeof e == "string" || (e && typeof e == "object");
}
function ea(e) {
  return typeof e == "string" || typeof e == "symbol";
}
const _t = {
    path: "/",
    name: void 0,
    params: {},
    query: {},
    hash: "",
    fullPath: "/",
    matched: [],
    meta: {},
    redirectedFrom: void 0,
  },
  ta = Symbol("");
var ci;
(function (e) {
  (e[(e.aborted = 4)] = "aborted"),
    (e[(e.cancelled = 8)] = "cancelled"),
    (e[(e.duplicated = 16)] = "duplicated");
})(ci || (ci = {}));
function cn(e, t) {
  return ue(new Error(), { type: e, [ta]: !0 }, t);
}
function ct(e, t) {
  return e instanceof Error && ta in e && (t == null || !!(e.type & t));
}
const ai = "[^/]+?",
  Nf = { sensitive: !1, strict: !1, start: !0, end: !0 },
  Mf = /[.+*?^${}()[\]/\\]/g;
function Ff(e, t) {
  const n = ue({}, Nf, t),
    o = [];
  let s = n.start ? "^" : "";
  const r = [];
  for (const l of e) {
    const u = l.length ? [] : [90];
    n.strict && !l.length && (s += "/");
    for (let f = 0; f < l.length; f++) {
      const d = l[f];
      let p = 40 + (n.sensitive ? 0.25 : 0);
      if (d.type === 0)
        f || (s += "/"), (s += d.value.replace(Mf, "\\$&")), (p += 40);
      else if (d.type === 1) {
        const { value: g, repeatable: y, optional: w, regexp: x } = d;
        r.push({ name: g, repeatable: y, optional: w });
        const v = x || ai;
        if (v !== ai) {
          p += 10;
          try {
            new RegExp(`(${v})`);
          } catch (R) {
            throw new Error(
              `Invalid custom RegExp for param "${g}" (${v}): ` + R.message
            );
          }
        }
        let O = y ? `((?:${v})(?:/(?:${v}))*)` : `(${v})`;
        f || (O = w && l.length < 2 ? `(?:/${O})` : "/" + O),
          w && (O += "?"),
          (s += O),
          (p += 20),
          w && (p += -8),
          y && (p += -20),
          v === ".*" && (p += -50);
      }
      u.push(p);
    }
    o.push(u);
  }
  if (n.strict && n.end) {
    const l = o.length - 1;
    o[l][o[l].length - 1] += 0.7000000000000001;
  }
  n.strict || (s += "/?"), n.end ? (s += "$") : n.strict && (s += "(?:/|$)");
  const i = new RegExp(s, n.sensitive ? "" : "i");
  function c(l) {
    const u = l.match(i),
      f = {};
    if (!u) return null;
    for (let d = 1; d < u.length; d++) {
      const p = u[d] || "",
        g = r[d - 1];
      f[g.name] = p && g.repeatable ? p.split("/") : p;
    }
    return f;
  }
  function a(l) {
    let u = "",
      f = !1;
    for (const d of e) {
      (!f || !u.endsWith("/")) && (u += "/"), (f = !1);
      for (const p of d)
        if (p.type === 0) u += p.value;
        else if (p.type === 1) {
          const { value: g, repeatable: y, optional: w } = p,
            x = g in l ? l[g] : "";
          if (Je(x) && !y)
            throw new Error(
              `Provided param "${g}" is an array but it is not repeatable (* or + modifiers)`
            );
          const v = Je(x) ? x.join("/") : x;
          if (!v)
            if (w)
              d.length < 2 &&
                (u.endsWith("/") ? (u = u.slice(0, -1)) : (f = !0));
            else throw new Error(`Missing required param "${g}"`);
          u += v;
        }
    }
    return u || "/";
  }
  return { re: i, score: o, keys: r, parse: c, stringify: a };
}
function Df(e, t) {
  let n = 0;
  for (; n < e.length && n < t.length; ) {
    const o = t[n] - e[n];
    if (o) return o;
    n++;
  }
  return e.length < t.length
    ? e.length === 1 && e[0] === 40 + 40
      ? -1
      : 1
    : e.length > t.length
    ? t.length === 1 && t[0] === 40 + 40
      ? 1
      : -1
    : 0;
}
function Uf(e, t) {
  let n = 0;
  const o = e.score,
    s = t.score;
  for (; n < o.length && n < s.length; ) {
    const r = Df(o[n], s[n]);
    if (r) return r;
    n++;
  }
  if (Math.abs(s.length - o.length) === 1) {
    if (li(o)) return 1;
    if (li(s)) return -1;
  }
  return s.length - o.length;
}
function li(e) {
  const t = e[e.length - 1];
  return e.length > 0 && t[t.length - 1] < 0;
}
const zf = { type: 0, value: "" },
  Kf = /[a-zA-Z0-9_]/;
function Hf(e) {
  if (!e) return [[]];
  if (e === "/") return [[zf]];
  if (!e.startsWith("/")) throw new Error(`Invalid path "${e}"`);
  function t(p) {
    throw new Error(`ERR (${n})/"${l}": ${p}`);
  }
  let n = 0,
    o = n;
  const s = [];
  let r;
  function i() {
    r && s.push(r), (r = []);
  }
  let c = 0,
    a,
    l = "",
    u = "";
  function f() {
    l &&
      (n === 0
        ? r.push({ type: 0, value: l })
        : n === 1 || n === 2 || n === 3
        ? (r.length > 1 &&
            (a === "*" || a === "+") &&
            t(
              `A repeatable param (${l}) must be alone in its segment. eg: '/:ids+.`
            ),
          r.push({
            type: 1,
            value: l,
            regexp: u,
            repeatable: a === "*" || a === "+",
            optional: a === "*" || a === "?",
          }))
        : t("Invalid state to consume buffer"),
      (l = ""));
  }
  function d() {
    l += a;
  }
  for (; c < e.length; ) {
    if (((a = e[c++]), a === "\\" && n !== 2)) {
      (o = n), (n = 4);
      continue;
    }
    switch (n) {
      case 0:
        a === "/" ? (l && f(), i()) : a === ":" ? (f(), (n = 1)) : d();
        break;
      case 4:
        d(), (n = o);
        break;
      case 1:
        a === "("
          ? (n = 2)
          : Kf.test(a)
          ? d()
          : (f(), (n = 0), a !== "*" && a !== "?" && a !== "+" && c--);
        break;
      case 2:
        a === ")"
          ? u[u.length - 1] == "\\"
            ? (u = u.slice(0, -1) + a)
            : (n = 3)
          : (u += a);
        break;
      case 3:
        f(), (n = 0), a !== "*" && a !== "?" && a !== "+" && c--, (u = "");
        break;
      default:
        t("Unknown state");
        break;
    }
  }
  return n === 2 && t(`Unfinished custom RegExp for param "${l}"`), f(), i(), s;
}
function Bf(e, t, n) {
  const o = Ff(Hf(e.path), n),
    s = ue(o, { record: e, parent: t, children: [], alias: [] });
  return t && !s.record.aliasOf == !t.record.aliasOf && t.children.push(s), s;
}
function Wf(e, t) {
  const n = [],
    o = new Map();
  t = di({ strict: !1, end: !0, sensitive: !1 }, t);
  function s(u) {
    return o.get(u);
  }
  function r(u, f, d) {
    const p = !d,
      g = Vf(u);
    g.aliasOf = d && d.record;
    const y = di(t, u),
      w = [g];
    if ("alias" in u) {
      const O = typeof u.alias == "string" ? [u.alias] : u.alias;
      for (const R of O)
        w.push(
          ue({}, g, {
            components: d ? d.record.components : g.components,
            path: R,
            aliasOf: d ? d.record : g,
          })
        );
    }
    let x, v;
    for (const O of w) {
      const { path: R } = O;
      if (f && R[0] !== "/") {
        const U = f.record.path,
          F = U[U.length - 1] === "/" ? "" : "/";
        O.path = f.record.path + (R && F + R);
      }
      if (
        ((x = Bf(O, f, y)),
        d
          ? d.alias.push(x)
          : ((v = v || x),
            v !== x && v.alias.push(x),
            p && u.name && !fi(x) && i(u.name)),
        g.children)
      ) {
        const U = g.children;
        for (let F = 0; F < U.length; F++) r(U[F], x, d && d.children[F]);
      }
      (d = d || x),
        ((x.record.components && Object.keys(x.record.components).length) ||
          x.record.name ||
          x.record.redirect) &&
          a(x);
    }
    return v
      ? () => {
          i(v);
        }
      : Cn;
  }
  function i(u) {
    if (ea(u)) {
      const f = o.get(u);
      f &&
        (o.delete(u),
        n.splice(n.indexOf(f), 1),
        f.children.forEach(i),
        f.alias.forEach(i));
    } else {
      const f = n.indexOf(u);
      f > -1 &&
        (n.splice(f, 1),
        u.record.name && o.delete(u.record.name),
        u.children.forEach(i),
        u.alias.forEach(i));
    }
  }
  function c() {
    return n;
  }
  function a(u) {
    let f = 0;
    for (
      ;
      f < n.length &&
      Uf(u, n[f]) >= 0 &&
      (u.record.path !== n[f].record.path || !na(u, n[f]));

    )
      f++;
    n.splice(f, 0, u), u.record.name && !fi(u) && o.set(u.record.name, u);
  }
  function l(u, f) {
    let d,
      p = {},
      g,
      y;
    if ("name" in u && u.name) {
      if (((d = o.get(u.name)), !d)) throw cn(1, { location: u });
      (y = d.record.name),
        (p = ue(
          ui(
            f.params,
            d.keys.filter((v) => !v.optional).map((v) => v.name)
          ),
          u.params &&
            ui(
              u.params,
              d.keys.map((v) => v.name)
            )
        )),
        (g = d.stringify(p));
    } else if ("path" in u)
      (g = u.path),
        (d = n.find((v) => v.re.test(g))),
        d && ((p = d.parse(g)), (y = d.record.name));
    else {
      if (((d = f.name ? o.get(f.name) : n.find((v) => v.re.test(f.path))), !d))
        throw cn(1, { location: u, currentLocation: f });
      (y = d.record.name),
        (p = ue({}, f.params, u.params)),
        (g = d.stringify(p));
    }
    const w = [];
    let x = d;
    for (; x; ) w.unshift(x.record), (x = x.parent);
    return { name: y, path: g, params: p, matched: w, meta: qf(w) };
  }
  return (
    e.forEach((u) => r(u)),
    {
      addRoute: r,
      resolve: l,
      removeRoute: i,
      getRoutes: c,
      getRecordMatcher: s,
    }
  );
}
function ui(e, t) {
  const n = {};
  for (const o of t) o in e && (n[o] = e[o]);
  return n;
}
function Vf(e) {
  return {
    path: e.path,
    redirect: e.redirect,
    name: e.name,
    meta: e.meta || {},
    aliasOf: void 0,
    beforeEnter: e.beforeEnter,
    props: Zf(e),
    children: e.children || [],
    instances: {},
    leaveGuards: new Set(),
    updateGuards: new Set(),
    enterCallbacks: {},
    components:
      "components" in e
        ? e.components || null
        : e.component && { default: e.component },
  };
}
function Zf(e) {
  const t = {},
    n = e.props || !1;
  if ("component" in e) t.default = n;
  else for (const o in e.components) t[o] = typeof n == "boolean" ? n : n[o];
  return t;
}
function fi(e) {
  for (; e; ) {
    if (e.record.aliasOf) return !0;
    e = e.parent;
  }
  return !1;
}
function qf(e) {
  return e.reduce((t, n) => ue(t, n.meta), {});
}
function di(e, t) {
  const n = {};
  for (const o in e) n[o] = o in t ? t[o] : e[o];
  return n;
}
function na(e, t) {
  return t.children.some((n) => n === e || na(e, n));
}
const oa = /#/g,
  Xf = /&/g,
  Jf = /\//g,
  Gf = /=/g,
  Yf = /\?/g,
  sa = /\+/g,
  Qf = /%5B/g,
  ed = /%5D/g,
  ra = /%5E/g,
  td = /%60/g,
  ia = /%7B/g,
  nd = /%7C/g,
  ca = /%7D/g,
  od = /%20/g;
function Qs(e) {
  return encodeURI("" + e)
    .replace(nd, "|")
    .replace(Qf, "[")
    .replace(ed, "]");
}
function sd(e) {
  return Qs(e).replace(ia, "{").replace(ca, "}").replace(ra, "^");
}
function _s(e) {
  return Qs(e)
    .replace(sa, "%2B")
    .replace(od, "+")
    .replace(oa, "%23")
    .replace(Xf, "%26")
    .replace(td, "`")
    .replace(ia, "{")
    .replace(ca, "}")
    .replace(ra, "^");
}
function rd(e) {
  return _s(e).replace(Gf, "%3D");
}
function id(e) {
  return Qs(e).replace(oa, "%23").replace(Yf, "%3F");
}
function cd(e) {
  return e == null ? "" : id(e).replace(Jf, "%2F");
}
function po(e) {
  try {
    return decodeURIComponent("" + e);
  } catch {}
  return "" + e;
}
function ad(e) {
  const t = {};
  if (e === "" || e === "?") return t;
  const o = (e[0] === "?" ? e.slice(1) : e).split("&");
  for (let s = 0; s < o.length; ++s) {
    const r = o[s].replace(sa, " "),
      i = r.indexOf("="),
      c = po(i < 0 ? r : r.slice(0, i)),
      a = i < 0 ? null : po(r.slice(i + 1));
    if (c in t) {
      let l = t[c];
      Je(l) || (l = t[c] = [l]), l.push(a);
    } else t[c] = a;
  }
  return t;
}
function hi(e) {
  let t = "";
  for (let n in e) {
    const o = e[n];
    if (((n = rd(n)), o == null)) {
      o !== void 0 && (t += (t.length ? "&" : "") + n);
      continue;
    }
    (Je(o) ? o.map((r) => r && _s(r)) : [o && _s(o)]).forEach((r) => {
      r !== void 0 &&
        ((t += (t.length ? "&" : "") + n), r != null && (t += "=" + r));
    });
  }
  return t;
}
function ld(e) {
  const t = {};
  for (const n in e) {
    const o = e[n];
    o !== void 0 &&
      (t[n] = Je(o)
        ? o.map((s) => (s == null ? null : "" + s))
        : o == null
        ? o
        : "" + o);
  }
  return t;
}
const ud = Symbol(""),
  pi = Symbol(""),
  er = Symbol(""),
  aa = Symbol(""),
  ys = Symbol("");
function hn() {
  let e = [];
  function t(o) {
    return (
      e.push(o),
      () => {
        const s = e.indexOf(o);
        s > -1 && e.splice(s, 1);
      }
    );
  }
  function n() {
    e = [];
  }
  return { add: t, list: () => e, reset: n };
}
function bt(e, t, n, o, s) {
  const r = o && (o.enterCallbacks[s] = o.enterCallbacks[s] || []);
  return () =>
    new Promise((i, c) => {
      const a = (f) => {
          f === !1
            ? c(cn(4, { from: n, to: t }))
            : f instanceof Error
            ? c(f)
            : Lf(f)
            ? c(cn(2, { from: t, to: f }))
            : (r &&
                o.enterCallbacks[s] === r &&
                typeof f == "function" &&
                r.push(f),
              i());
        },
        l = e.call(o && o.instances[s], t, n, a);
      let u = Promise.resolve(l);
      e.length < 3 && (u = u.then(a)), u.catch((f) => c(f));
    });
}
function Vo(e, t, n, o) {
  const s = [];
  for (const r of e)
    for (const i in r.components) {
      let c = r.components[i];
      if (!(t !== "beforeRouteEnter" && !r.instances[i]))
        if (fd(c)) {
          const l = (c.__vccOpts || c)[t];
          l && s.push(bt(l, n, o, r, i));
        } else {
          let a = c();
          s.push(() =>
            a.then((l) => {
              if (!l)
                return Promise.reject(
                  new Error(`Couldn't resolve component "${i}" at "${r.path}"`)
                );
              const u = _f(l) ? l.default : l;
              r.components[i] = u;
              const d = (u.__vccOpts || u)[t];
              return d && bt(d, n, o, r, i)();
            })
          );
        }
    }
  return s;
}
function fd(e) {
  return (
    typeof e == "object" ||
    "displayName" in e ||
    "props" in e ||
    "__vccOpts" in e
  );
}
function mi(e) {
  const t = Xe(er),
    n = Xe(aa),
    o = Oe(() => t.resolve(z(e.to))),
    s = Oe(() => {
      const { matched: a } = o.value,
        { length: l } = a,
        u = a[l - 1],
        f = n.matched;
      if (!u || !f.length) return -1;
      const d = f.findIndex(rn.bind(null, u));
      if (d > -1) return d;
      const p = gi(a[l - 2]);
      return l > 1 && gi(u) === p && f[f.length - 1].path !== p
        ? f.findIndex(rn.bind(null, a[l - 2]))
        : d;
    }),
    r = Oe(() => s.value > -1 && md(n.params, o.value.params)),
    i = Oe(
      () =>
        s.value > -1 &&
        s.value === n.matched.length - 1 &&
        Yc(n.params, o.value.params)
    );
  function c(a = {}) {
    return pd(a)
      ? t[z(e.replace) ? "replace" : "push"](z(e.to)).catch(Cn)
      : Promise.resolve();
  }
  return {
    route: o,
    href: Oe(() => o.value.href),
    isActive: r,
    isExactActive: i,
    navigate: c,
  };
}
const dd = $e({
    name: "RouterLink",
    compatConfig: { MODE: 3 },
    props: {
      to: { type: [String, Object], required: !0 },
      replace: Boolean,
      activeClass: String,
      exactActiveClass: String,
      custom: Boolean,
      ariaCurrentValue: { type: String, default: "page" },
    },
    useLink: mi,
    setup(e, { slots: t }) {
      const n = st(mi(e)),
        { options: o } = Xe(er),
        s = Oe(() => ({
          [_i(e.activeClass, o.linkActiveClass, "router-link-active")]:
            n.isActive,
          [_i(
            e.exactActiveClass,
            o.linkExactActiveClass,
            "router-link-exact-active"
          )]: n.isExactActive,
        }));
      return () => {
        const r = t.default && t.default(n);
        return e.custom
          ? r
          : Ln(
              "a",
              {
                "aria-current": n.isExactActive ? e.ariaCurrentValue : null,
                href: n.href,
                onClick: n.navigate,
                class: s.value,
              },
              r
            );
      };
    },
  }),
  hd = dd;
function pd(e) {
  if (
    !(e.metaKey || e.altKey || e.ctrlKey || e.shiftKey) &&
    !e.defaultPrevented &&
    !(e.button !== void 0 && e.button !== 0)
  ) {
    if (e.currentTarget && e.currentTarget.getAttribute) {
      const t = e.currentTarget.getAttribute("target");
      if (/\b_blank\b/i.test(t)) return;
    }
    return e.preventDefault && e.preventDefault(), !0;
  }
}
function md(e, t) {
  for (const n in t) {
    const o = t[n],
      s = e[n];
    if (typeof o == "string") {
      if (o !== s) return !1;
    } else if (!Je(s) || s.length !== o.length || o.some((r, i) => r !== s[i]))
      return !1;
  }
  return !0;
}
function gi(e) {
  return e ? (e.aliasOf ? e.aliasOf.path : e.path) : "";
}
const _i = (e, t, n) => e ?? t ?? n,
  gd = $e({
    name: "RouterView",
    inheritAttrs: !1,
    props: { name: { type: String, default: "default" }, route: Object },
    compatConfig: { MODE: 3 },
    setup(e, { attrs: t, slots: n }) {
      const o = Xe(ys),
        s = Oe(() => e.route || o.value),
        r = Xe(pi, 0),
        i = Oe(() => {
          let l = z(r);
          const { matched: u } = s.value;
          let f;
          for (; (f = u[l]) && !f.components; ) l++;
          return l;
        }),
        c = Oe(() => s.value.matched[i.value]);
      eo(
        pi,
        Oe(() => i.value + 1)
      ),
        eo(ud, c),
        eo(ys, s);
      const a = se();
      return (
        Ee(
          () => [a.value, c.value, e.name],
          ([l, u, f], [d, p, g]) => {
            u &&
              ((u.instances[f] = l),
              p &&
                p !== u &&
                l &&
                l === d &&
                (u.leaveGuards.size || (u.leaveGuards = p.leaveGuards),
                u.updateGuards.size || (u.updateGuards = p.updateGuards))),
              l &&
                u &&
                (!p || !rn(u, p) || !d) &&
                (u.enterCallbacks[f] || []).forEach((y) => y(l));
          },
          { flush: "post" }
        ),
        () => {
          const l = s.value,
            u = e.name,
            f = c.value,
            d = f && f.components[u];
          if (!d) return yi(n.default, { Component: d, route: l });
          const p = f.props[u],
            g = p
              ? p === !0
                ? l.params
                : typeof p == "function"
                ? p(l)
                : p
              : null,
            w = Ln(
              d,
              ue({}, g, t, {
                onVnodeUnmounted: (x) => {
                  x.component.isUnmounted && (f.instances[u] = null);
                },
                ref: a,
              })
            );
          return yi(n.default, { Component: w, route: l }) || w;
        }
      );
    },
  });
function yi(e, t) {
  if (!e) return null;
  const n = e(t);
  return n.length === 1 ? n[0] : n;
}
const _d = gd;
function yd(e) {
  const t = Wf(e.routes, e),
    n = e.parseQuery || ad,
    o = e.stringifyQuery || hi,
    s = e.history,
    r = hn(),
    i = hn(),
    c = hn(),
    a = Qn(_t);
  let l = _t;
  Jt &&
    e.scrollBehavior &&
    "scrollRestoration" in history &&
    (history.scrollRestoration = "manual");
  const u = Bo.bind(null, (k) => "" + k),
    f = Bo.bind(null, cd),
    d = Bo.bind(null, po);
  function p(k, M) {
    let j, K;
    return (
      ea(k) ? ((j = t.getRecordMatcher(k)), (K = M)) : (K = k), t.addRoute(K, j)
    );
  }
  function g(k) {
    const M = t.getRecordMatcher(k);
    M && t.removeRoute(M);
  }
  function y() {
    return t.getRoutes().map((k) => k.record);
  }
  function w(k) {
    return !!t.getRecordMatcher(k);
  }
  function x(k, M) {
    if (((M = ue({}, M || a.value)), typeof k == "string")) {
      const _ = Wo(n, k, M.path),
        b = t.resolve({ path: _.path }, M),
        C = s.createHref(_.fullPath);
      return ue(_, b, {
        params: d(b.params),
        hash: po(_.hash),
        redirectedFrom: void 0,
        href: C,
      });
    }
    let j;
    if ("path" in k) j = ue({}, k, { path: Wo(n, k.path, M.path).path });
    else {
      const _ = ue({}, k.params);
      for (const b in _) _[b] == null && delete _[b];
      (j = ue({}, k, { params: f(_) })), (M.params = f(M.params));
    }
    const K = t.resolve(j, M),
      le = k.hash || "";
    K.params = u(d(K.params));
    const h = bf(o, ue({}, k, { hash: sd(le), path: K.path })),
      m = s.createHref(h);
    return ue(
      { fullPath: h, hash: le, query: o === hi ? ld(k.query) : k.query || {} },
      K,
      { redirectedFrom: void 0, href: m }
    );
  }
  function v(k) {
    return typeof k == "string" ? Wo(n, k, a.value.path) : ue({}, k);
  }
  function O(k, M) {
    if (l !== k) return cn(8, { from: M, to: k });
  }
  function R(k) {
    return N(k);
  }
  function U(k) {
    return R(ue(v(k), { replace: !0 }));
  }
  function F(k) {
    const M = k.matched[k.matched.length - 1];
    if (M && M.redirect) {
      const { redirect: j } = M;
      let K = typeof j == "function" ? j(k) : j;
      return (
        typeof K == "string" &&
          ((K = K.includes("?") || K.includes("#") ? (K = v(K)) : { path: K }),
          (K.params = {})),
        ue(
          { query: k.query, hash: k.hash, params: "path" in K ? {} : k.params },
          K
        )
      );
    }
  }
  function N(k, M) {
    const j = (l = x(k)),
      K = a.value,
      le = k.state,
      h = k.force,
      m = k.replace === !0,
      _ = F(j);
    if (_)
      return N(
        ue(v(_), {
          state: typeof _ == "object" ? ue({}, le, _.state) : le,
          force: h,
          replace: m,
        }),
        M || j
      );
    const b = j;
    b.redirectedFrom = M;
    let C;
    return (
      !h && wf(o, K, j) && ((C = cn(16, { to: b, from: K })), Ae(K, K, !0, !1)),
      (C ? Promise.resolve(C) : q(b, K))
        .catch((I) => (ct(I) ? (ct(I, 2) ? I : Ie(I)) : te(I, b, K)))
        .then((I) => {
          if (I) {
            if (ct(I, 2))
              return N(
                ue({ replace: m }, v(I.to), {
                  state: typeof I.to == "object" ? ue({}, le, I.to.state) : le,
                  force: h,
                }),
                M || b
              );
          } else I = L(b, K, !0, m, le);
          return ae(b, K, I), I;
        })
    );
  }
  function T(k, M) {
    const j = O(k, M);
    return j ? Promise.reject(j) : Promise.resolve();
  }
  function Z(k) {
    const M = ye.values().next().value;
    return M && typeof M.runWithContext == "function"
      ? M.runWithContext(k)
      : k();
  }
  function q(k, M) {
    let j;
    const [K, le, h] = vd(k, M);
    j = Vo(K.reverse(), "beforeRouteLeave", k, M);
    for (const _ of K)
      _.leaveGuards.forEach((b) => {
        j.push(bt(b, k, M));
      });
    const m = T.bind(null, k, M);
    return (
      j.push(m),
      Pe(j)
        .then(() => {
          j = [];
          for (const _ of r.list()) j.push(bt(_, k, M));
          return j.push(m), Pe(j);
        })
        .then(() => {
          j = Vo(le, "beforeRouteUpdate", k, M);
          for (const _ of le)
            _.updateGuards.forEach((b) => {
              j.push(bt(b, k, M));
            });
          return j.push(m), Pe(j);
        })
        .then(() => {
          j = [];
          for (const _ of k.matched)
            if (_.beforeEnter && !M.matched.includes(_))
              if (Je(_.beforeEnter))
                for (const b of _.beforeEnter) j.push(bt(b, k, M));
              else j.push(bt(_.beforeEnter, k, M));
          return j.push(m), Pe(j);
        })
        .then(
          () => (
            k.matched.forEach((_) => (_.enterCallbacks = {})),
            (j = Vo(h, "beforeRouteEnter", k, M)),
            j.push(m),
            Pe(j)
          )
        )
        .then(() => {
          j = [];
          for (const _ of i.list()) j.push(bt(_, k, M));
          return j.push(m), Pe(j);
        })
        .catch((_) => (ct(_, 8) ? _ : Promise.reject(_)))
    );
  }
  function ae(k, M, j) {
    for (const K of c.list()) Z(() => K(k, M, j));
  }
  function L(k, M, j, K, le) {
    const h = O(k, M);
    if (h) return h;
    const m = M === _t,
      _ = Jt ? history.state : {};
    j &&
      (K || m
        ? s.replace(k.fullPath, ue({ scroll: m && _ && _.scroll }, le))
        : s.push(k.fullPath, le)),
      (a.value = k),
      Ae(k, M, j, m),
      Ie();
  }
  let oe;
  function de() {
    oe ||
      (oe = s.listen((k, M, j) => {
        if (!Tt.listening) return;
        const K = x(k),
          le = F(K);
        if (le) {
          N(ue(le, { replace: !0 }), K).catch(Cn);
          return;
        }
        l = K;
        const h = a.value;
        Jt && Tf(ri(h.fullPath, j.delta), To()),
          q(K, h)
            .catch((m) =>
              ct(m, 12)
                ? m
                : ct(m, 2)
                ? (N(m.to, K)
                    .then((_) => {
                      ct(_, 20) &&
                        !j.delta &&
                        j.type === Nn.pop &&
                        s.go(-1, !1);
                    })
                    .catch(Cn),
                  Promise.reject())
                : (j.delta && s.go(-j.delta, !1), te(m, K, h))
            )
            .then((m) => {
              (m = m || L(K, h, !1)),
                m &&
                  (j.delta && !ct(m, 8)
                    ? s.go(-j.delta, !1)
                    : j.type === Nn.pop && ct(m, 20) && s.go(-1, !1)),
                ae(K, h, m);
            })
            .catch(Cn);
      }));
  }
  let ee = hn(),
    ce = hn(),
    Q;
  function te(k, M, j) {
    Ie(k);
    const K = ce.list();
    return (
      K.length ? K.forEach((le) => le(k, M, j)) : console.error(k),
      Promise.reject(k)
    );
  }
  function xe() {
    return Q && a.value !== _t
      ? Promise.resolve()
      : new Promise((k, M) => {
          ee.add([k, M]);
        });
  }
  function Ie(k) {
    return (
      Q ||
        ((Q = !k),
        de(),
        ee.list().forEach(([M, j]) => (k ? j(k) : M())),
        ee.reset()),
      k
    );
  }
  function Ae(k, M, j, K) {
    const { scrollBehavior: le } = e;
    if (!Jt || !le) return Promise.resolve();
    const h =
      (!j && Pf(ri(k.fullPath, 0))) ||
      ((K || !j) && history.state && history.state.scroll) ||
      null;
    return Bs()
      .then(() => le(k, M, h))
      .then((m) => m && Of(m))
      .catch((m) => te(m, k, M));
  }
  const ke = (k) => s.go(k);
  let it;
  const ye = new Set(),
    Tt = {
      currentRoute: a,
      listening: !0,
      addRoute: p,
      removeRoute: g,
      hasRoute: w,
      getRoutes: y,
      resolve: x,
      options: e,
      push: R,
      replace: U,
      go: ke,
      back: () => ke(-1),
      forward: () => ke(1),
      beforeEach: r.add,
      beforeResolve: i.add,
      afterEach: c.add,
      onError: ce.add,
      isReady: xe,
      install(k) {
        const M = this;
        k.component("RouterLink", hd),
          k.component("RouterView", _d),
          (k.config.globalProperties.$router = M),
          Object.defineProperty(k.config.globalProperties, "$route", {
            enumerable: !0,
            get: () => z(a),
          }),
          Jt &&
            !it &&
            a.value === _t &&
            ((it = !0), R(s.location).catch((le) => {}));
        const j = {};
        for (const le in _t) j[le] = Oe(() => a.value[le]);
        k.provide(er, M), k.provide(aa, st(j)), k.provide(ys, a);
        const K = k.unmount;
        ye.add(k),
          (k.unmount = function () {
            ye.delete(k),
              ye.size < 1 &&
                ((l = _t),
                oe && oe(),
                (oe = null),
                (a.value = _t),
                (it = !1),
                (Q = !1)),
              K();
          });
      },
    };
  function Pe(k) {
    return k.reduce((M, j) => M.then(() => Z(j)), Promise.resolve());
  }
  return Tt;
}
function vd(e, t) {
  const n = [],
    o = [],
    s = [],
    r = Math.max(t.matched.length, e.matched.length);
  for (let i = 0; i < r; i++) {
    const c = t.matched[i];
    c && (e.matched.find((l) => rn(l, c)) ? o.push(c) : n.push(c));
    const a = e.matched[i];
    a && (t.matched.find((l) => rn(l, a)) || s.push(a));
  }
  return [n, o, s];
}
var bd = !1;
/*!
 * pinia v2.0.36
 * (c) 2023 Eduardo San Martin Morote
 * @license MIT
 */ let la;
const Po = (e) => (la = e),
  ua = Symbol();
function vs(e) {
  return (
    e &&
    typeof e == "object" &&
    Object.prototype.toString.call(e) === "[object Object]" &&
    typeof e.toJSON != "function"
  );
}
var Sn;
(function (e) {
  (e.direct = "direct"),
    (e.patchObject = "patch object"),
    (e.patchFunction = "patch function");
})(Sn || (Sn = {}));
function wd() {
  const e = oc(!0),
    t = e.run(() => se({}));
  let n = [],
    o = [];
  const s = on({
    install(r) {
      Po(s),
        (s._a = r),
        r.provide(ua, s),
        (r.config.globalProperties.$pinia = s),
        o.forEach((i) => n.push(i)),
        (o = []);
    },
    use(r) {
      return !this._a && !bd ? o.push(r) : n.push(r), this;
    },
    _p: n,
    _a: null,
    _e: e,
    _s: new Map(),
    state: t,
  });
  return s;
}
const fa = () => {};
function vi(e, t, n, o = fa) {
  e.push(t);
  const s = () => {
    const r = e.indexOf(t);
    r > -1 && (e.splice(r, 1), o());
  };
  return !n && Ls() && sc(s), s;
}
function qt(e, ...t) {
  e.slice().forEach((n) => {
    n(...t);
  });
}
function bs(e, t) {
  e instanceof Map && t instanceof Map && t.forEach((n, o) => e.set(o, n)),
    e instanceof Set && t instanceof Set && t.forEach(e.add, e);
  for (const n in t) {
    if (!t.hasOwnProperty(n)) continue;
    const o = t[n],
      s = e[n];
    vs(s) && vs(o) && e.hasOwnProperty(n) && !ge(o) && !xt(o)
      ? (e[n] = bs(s, o))
      : (e[n] = o);
  }
  return e;
}
const xd = Symbol();
function kd(e) {
  return !vs(e) || !e.hasOwnProperty(xd);
}
const { assign: yt } = Object;
function Cd(e) {
  return !!(ge(e) && e.effect);
}
function Id(e, t, n, o) {
  const { state: s, actions: r, getters: i } = t,
    c = n.state.value[e];
  let a;
  function l() {
    c || (n.state.value[e] = s ? s() : {});
    const u = Ol(n.state.value[e]);
    return yt(
      u,
      r,
      Object.keys(i || {}).reduce(
        (f, d) => (
          (f[d] = on(
            Oe(() => {
              Po(n);
              const p = n._s.get(e);
              return i[d].call(p, p);
            })
          )),
          f
        ),
        {}
      )
    );
  }
  return (a = da(e, l, t, n, o, !0)), a;
}
function da(e, t, n = {}, o, s, r) {
  let i;
  const c = yt({ actions: {} }, n),
    a = { deep: !0 };
  let l,
    u,
    f = on([]),
    d = on([]),
    p;
  const g = o.state.value[e];
  !r && !g && (o.state.value[e] = {}), se({});
  let y;
  function w(N) {
    let T;
    (l = u = !1),
      typeof N == "function"
        ? (N(o.state.value[e]),
          (T = { type: Sn.patchFunction, storeId: e, events: p }))
        : (bs(o.state.value[e], N),
          (T = { type: Sn.patchObject, payload: N, storeId: e, events: p }));
    const Z = (y = Symbol());
    Bs().then(() => {
      y === Z && (l = !0);
    }),
      (u = !0),
      qt(f, T, o.state.value[e]);
  }
  const x = r
    ? function () {
        const { state: T } = n,
          Z = T ? T() : {};
        this.$patch((q) => {
          yt(q, Z);
        });
      }
    : fa;
  function v() {
    i.stop(), (f = []), (d = []), o._s.delete(e);
  }
  function O(N, T) {
    return function () {
      Po(o);
      const Z = Array.from(arguments),
        q = [],
        ae = [];
      function L(ee) {
        q.push(ee);
      }
      function oe(ee) {
        ae.push(ee);
      }
      qt(d, { args: Z, name: N, store: U, after: L, onError: oe });
      let de;
      try {
        de = T.apply(this && this.$id === e ? this : U, Z);
      } catch (ee) {
        throw (qt(ae, ee), ee);
      }
      return de instanceof Promise
        ? de
            .then((ee) => (qt(q, ee), ee))
            .catch((ee) => (qt(ae, ee), Promise.reject(ee)))
        : (qt(q, de), de);
    };
  }
  const R = {
      _p: o,
      $id: e,
      $onAction: vi.bind(null, d),
      $patch: w,
      $reset: x,
      $subscribe(N, T = {}) {
        const Z = vi(f, N, T.detached, () => q()),
          q = i.run(() =>
            Ee(
              () => o.state.value[e],
              (ae) => {
                (T.flush === "sync" ? u : l) &&
                  N({ storeId: e, type: Sn.direct, events: p }, ae);
              },
              yt({}, a, T)
            )
          );
        return Z;
      },
      $dispose: v,
    },
    U = st(R);
  o._s.set(e, U);
  const F = o._e.run(() => ((i = oc()), i.run(() => t())));
  for (const N in F) {
    const T = F[N];
    if ((ge(T) && !Cd(T)) || xt(T))
      r ||
        (g && kd(T) && (ge(T) ? (T.value = g[N]) : bs(T, g[N])),
        (o.state.value[e][N] = T));
    else if (typeof T == "function") {
      const Z = O(N, T);
      (F[N] = Z), (c.actions[N] = T);
    }
  }
  return (
    yt(U, F),
    yt(re(U), F),
    Object.defineProperty(U, "$state", {
      get: () => o.state.value[e],
      set: (N) => {
        w((T) => {
          yt(T, N);
        });
      },
    }),
    o._p.forEach((N) => {
      yt(
        U,
        i.run(() => N({ store: U, app: o._a, pinia: o, options: c }))
      );
    }),
    g && r && n.hydrate && n.hydrate(U.$state, g),
    (l = !0),
    (u = !0),
    U
  );
}
function Sd(e, t, n) {
  let o, s;
  const r = typeof t == "function";
  typeof e == "string" ? ((o = e), (s = r ? n : t)) : ((s = e), (o = e.id));
  function i(c, a) {
    const l = Vc();
    return (
      (c = c || (l && Xe(ua, null))),
      c && Po(c),
      (c = la),
      c._s.has(o) || (r ? da(o, t, s, c) : Id(o, s, c)),
      c._s.get(o)
    );
  }
  return (i.$id = o), i;
}
const ha = Symbol("$auth0");
function et(e, t) {
  var n = {};
  for (var o in e)
    Object.prototype.hasOwnProperty.call(e, o) &&
      t.indexOf(o) < 0 &&
      (n[o] = e[o]);
  if (e != null && typeof Object.getOwnPropertySymbols == "function") {
    var s = 0;
    for (o = Object.getOwnPropertySymbols(e); s < o.length; s++)
      t.indexOf(o[s]) < 0 &&
        Object.prototype.propertyIsEnumerable.call(e, o[s]) &&
        (n[o[s]] = e[o[s]]);
  }
  return n;
}
var Yt =
  typeof globalThis < "u"
    ? globalThis
    : typeof window < "u"
    ? window
    : typeof global < "u"
    ? global
    : typeof self < "u"
    ? self
    : {};
function tr(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default")
    ? e.default
    : e;
}
function nr(e, t) {
  return e((t = { exports: {} }), t.exports), t.exports;
}
var $t = nr(function (e, t) {
  Object.defineProperty(t, "__esModule", { value: !0 });
  var n = (function () {
    function o() {
      var s = this;
      (this.locked = new Map()),
        (this.addToLocked = function (r, i) {
          var c = s.locked.get(r);
          c === void 0
            ? i === void 0
              ? s.locked.set(r, [])
              : s.locked.set(r, [i])
            : i !== void 0 && (c.unshift(i), s.locked.set(r, c));
        }),
        (this.isLocked = function (r) {
          return s.locked.has(r);
        }),
        (this.lock = function (r) {
          return new Promise(function (i, c) {
            s.isLocked(r) ? s.addToLocked(r, i) : (s.addToLocked(r), i());
          });
        }),
        (this.unlock = function (r) {
          var i = s.locked.get(r);
          if (i !== void 0 && i.length !== 0) {
            var c = i.pop();
            s.locked.set(r, i), c !== void 0 && setTimeout(c, 0);
          } else s.locked.delete(r);
        });
    }
    return (
      (o.getInstance = function () {
        return o.instance === void 0 && (o.instance = new o()), o.instance;
      }),
      o
    );
  })();
  t.default = function () {
    return n.getInstance();
  };
});
tr($t);
var Ed = tr(
  nr(function (e, t) {
    var n =
        (Yt && Yt.__awaiter) ||
        function (a, l, u, f) {
          return new (u || (u = Promise))(function (d, p) {
            function g(x) {
              try {
                w(f.next(x));
              } catch (v) {
                p(v);
              }
            }
            function y(x) {
              try {
                w(f.throw(x));
              } catch (v) {
                p(v);
              }
            }
            function w(x) {
              x.done
                ? d(x.value)
                : new u(function (v) {
                    v(x.value);
                  }).then(g, y);
            }
            w((f = f.apply(a, l || [])).next());
          });
        },
      o =
        (Yt && Yt.__generator) ||
        function (a, l) {
          var u,
            f,
            d,
            p,
            g = {
              label: 0,
              sent: function () {
                if (1 & d[0]) throw d[1];
                return d[1];
              },
              trys: [],
              ops: [],
            };
          return (
            (p = { next: y(0), throw: y(1), return: y(2) }),
            typeof Symbol == "function" &&
              (p[Symbol.iterator] = function () {
                return this;
              }),
            p
          );
          function y(w) {
            return function (x) {
              return (function (v) {
                if (u) throw new TypeError("Generator is already executing.");
                for (; g; )
                  try {
                    if (
                      ((u = 1),
                      f &&
                        (d =
                          2 & v[0]
                            ? f.return
                            : v[0]
                            ? f.throw || ((d = f.return) && d.call(f), 0)
                            : f.next) &&
                        !(d = d.call(f, v[1])).done)
                    )
                      return d;
                    switch (((f = 0), d && (v = [2 & v[0], d.value]), v[0])) {
                      case 0:
                      case 1:
                        d = v;
                        break;
                      case 4:
                        return g.label++, { value: v[1], done: !1 };
                      case 5:
                        g.label++, (f = v[1]), (v = [0]);
                        continue;
                      case 7:
                        (v = g.ops.pop()), g.trys.pop();
                        continue;
                      default:
                        if (
                          !(
                            (d = (d = g.trys).length > 0 && d[d.length - 1]) ||
                            (v[0] !== 6 && v[0] !== 2)
                          )
                        ) {
                          g = 0;
                          continue;
                        }
                        if (
                          v[0] === 3 &&
                          (!d || (v[1] > d[0] && v[1] < d[3]))
                        ) {
                          g.label = v[1];
                          break;
                        }
                        if (v[0] === 6 && g.label < d[1]) {
                          (g.label = d[1]), (d = v);
                          break;
                        }
                        if (d && g.label < d[2]) {
                          (g.label = d[2]), g.ops.push(v);
                          break;
                        }
                        d[2] && g.ops.pop(), g.trys.pop();
                        continue;
                    }
                    v = l.call(a, g);
                  } catch (O) {
                    (v = [6, O]), (f = 0);
                  } finally {
                    u = d = 0;
                  }
                if (5 & v[0]) throw v[1];
                return { value: v[0] ? v[1] : void 0, done: !0 };
              })([w, x]);
            };
          }
        };
    Object.defineProperty(t, "__esModule", { value: !0 });
    var s = "browser-tabs-lock-key";
    function r(a) {
      return new Promise(function (l) {
        return setTimeout(l, a);
      });
    }
    function i(a) {
      for (
        var l = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz",
          u = "",
          f = 0;
        f < a;
        f++
      )
        u += l[Math.floor(Math.random() * l.length)];
      return u;
    }
    var c = (function () {
      function a() {
        (this.acquiredIatSet = new Set()),
          (this.id = Date.now().toString() + i(15)),
          (this.acquireLock = this.acquireLock.bind(this)),
          (this.releaseLock = this.releaseLock.bind(this)),
          (this.releaseLock__private__ =
            this.releaseLock__private__.bind(this)),
          (this.waitForSomethingToChange =
            this.waitForSomethingToChange.bind(this)),
          (this.refreshLockWhileAcquired =
            this.refreshLockWhileAcquired.bind(this)),
          a.waiters === void 0 && (a.waiters = []);
      }
      return (
        (a.prototype.acquireLock = function (l, u) {
          return (
            u === void 0 && (u = 5e3),
            n(this, void 0, void 0, function () {
              var f, d, p, g, y, w;
              return o(this, function (x) {
                switch (x.label) {
                  case 0:
                    (f = Date.now() + i(4)),
                      (d = Date.now() + u),
                      (p = s + "-" + l),
                      (g = window.localStorage),
                      (x.label = 1);
                  case 1:
                    return Date.now() < d ? [4, r(30)] : [3, 8];
                  case 2:
                    return (
                      x.sent(),
                      g.getItem(p) !== null
                        ? [3, 5]
                        : ((y = this.id + "-" + l + "-" + f),
                          [4, r(Math.floor(25 * Math.random()))])
                    );
                  case 3:
                    return (
                      x.sent(),
                      g.setItem(
                        p,
                        JSON.stringify({
                          id: this.id,
                          iat: f,
                          timeoutKey: y,
                          timeAcquired: Date.now(),
                          timeRefreshed: Date.now(),
                        })
                      ),
                      [4, r(30)]
                    );
                  case 4:
                    return (
                      x.sent(),
                      (w = g.getItem(p)) !== null &&
                      (w = JSON.parse(w)).id === this.id &&
                      w.iat === f
                        ? (this.acquiredIatSet.add(f),
                          this.refreshLockWhileAcquired(p, f),
                          [2, !0])
                        : [3, 7]
                    );
                  case 5:
                    return (
                      a.lockCorrector(), [4, this.waitForSomethingToChange(d)]
                    );
                  case 6:
                    x.sent(), (x.label = 7);
                  case 7:
                    return (f = Date.now() + i(4)), [3, 1];
                  case 8:
                    return [2, !1];
                }
              });
            })
          );
        }),
        (a.prototype.refreshLockWhileAcquired = function (l, u) {
          return n(this, void 0, void 0, function () {
            var f = this;
            return o(this, function (d) {
              return (
                setTimeout(function () {
                  return n(f, void 0, void 0, function () {
                    var p, g;
                    return o(this, function (y) {
                      switch (y.label) {
                        case 0:
                          return [4, $t.default().lock(u)];
                        case 1:
                          return (
                            y.sent(),
                            this.acquiredIatSet.has(u)
                              ? ((p = window.localStorage),
                                (g = p.getItem(l)) === null
                                  ? ($t.default().unlock(u), [2])
                                  : (((g = JSON.parse(g)).timeRefreshed =
                                      Date.now()),
                                    p.setItem(l, JSON.stringify(g)),
                                    $t.default().unlock(u),
                                    this.refreshLockWhileAcquired(l, u),
                                    [2]))
                              : ($t.default().unlock(u), [2])
                          );
                      }
                    });
                  });
                }, 1e3),
                [2]
              );
            });
          });
        }),
        (a.prototype.waitForSomethingToChange = function (l) {
          return n(this, void 0, void 0, function () {
            return o(this, function (u) {
              switch (u.label) {
                case 0:
                  return [
                    4,
                    new Promise(function (f) {
                      var d = !1,
                        p = Date.now(),
                        g = !1;
                      function y() {
                        if (
                          (g ||
                            (window.removeEventListener("storage", y),
                            a.removeFromWaiting(y),
                            clearTimeout(w),
                            (g = !0)),
                          !d)
                        ) {
                          d = !0;
                          var x = 50 - (Date.now() - p);
                          x > 0 ? setTimeout(f, x) : f();
                        }
                      }
                      window.addEventListener("storage", y), a.addToWaiting(y);
                      var w = setTimeout(y, Math.max(0, l - Date.now()));
                    }),
                  ];
                case 1:
                  return u.sent(), [2];
              }
            });
          });
        }),
        (a.addToWaiting = function (l) {
          this.removeFromWaiting(l), a.waiters !== void 0 && a.waiters.push(l);
        }),
        (a.removeFromWaiting = function (l) {
          a.waiters !== void 0 &&
            (a.waiters = a.waiters.filter(function (u) {
              return u !== l;
            }));
        }),
        (a.notifyWaiters = function () {
          a.waiters !== void 0 &&
            a.waiters.slice().forEach(function (l) {
              return l();
            });
        }),
        (a.prototype.releaseLock = function (l) {
          return n(this, void 0, void 0, function () {
            return o(this, function (u) {
              switch (u.label) {
                case 0:
                  return [4, this.releaseLock__private__(l)];
                case 1:
                  return [2, u.sent()];
              }
            });
          });
        }),
        (a.prototype.releaseLock__private__ = function (l) {
          return n(this, void 0, void 0, function () {
            var u, f, d;
            return o(this, function (p) {
              switch (p.label) {
                case 0:
                  return (
                    (u = window.localStorage),
                    (f = s + "-" + l),
                    (d = u.getItem(f)) === null
                      ? [2]
                      : (d = JSON.parse(d)).id !== this.id
                      ? [3, 2]
                      : [4, $t.default().lock(d.iat)]
                  );
                case 1:
                  p.sent(),
                    this.acquiredIatSet.delete(d.iat),
                    u.removeItem(f),
                    $t.default().unlock(d.iat),
                    a.notifyWaiters(),
                    (p.label = 2);
                case 2:
                  return [2];
              }
            });
          });
        }),
        (a.lockCorrector = function () {
          for (
            var l = Date.now() - 5e3,
              u = window.localStorage,
              f = Object.keys(u),
              d = !1,
              p = 0;
            p < f.length;
            p++
          ) {
            var g = f[p];
            if (g.includes(s)) {
              var y = u.getItem(g);
              y !== null &&
                (((y = JSON.parse(y)).timeRefreshed === void 0 &&
                  y.timeAcquired < l) ||
                  (y.timeRefreshed !== void 0 && y.timeRefreshed < l)) &&
                (u.removeItem(g), (d = !0));
            }
          }
          d && a.notifyWaiters();
        }),
        (a.waiters = void 0),
        a
      );
    })();
    t.default = c;
  })
);
const Od = { timeoutInSeconds: 60 },
  pa = { name: "auth0-spa-js", version: "2.0.4" },
  ma = () => Date.now();
class He extends Error {
  constructor(t, n) {
    super(n),
      (this.error = t),
      (this.error_description = n),
      Object.setPrototypeOf(this, He.prototype);
  }
  static fromPayload({ error: t, error_description: n }) {
    return new He(t, n);
  }
}
class or extends He {
  constructor(t, n, o, s = null) {
    super(t, n),
      (this.state = o),
      (this.appState = s),
      Object.setPrototypeOf(this, or.prototype);
  }
}
class Mn extends He {
  constructor() {
    super("timeout", "Timeout"), Object.setPrototypeOf(this, Mn.prototype);
  }
}
class sr extends Mn {
  constructor(t) {
    super(), (this.popup = t), Object.setPrototypeOf(this, sr.prototype);
  }
}
class rr extends He {
  constructor(t) {
    super("cancelled", "Popup closed"),
      (this.popup = t),
      Object.setPrototypeOf(this, rr.prototype);
  }
}
class ir extends He {
  constructor(t, n, o) {
    super(t, n),
      (this.mfa_token = o),
      Object.setPrototypeOf(this, ir.prototype);
  }
}
class Ro extends He {
  constructor(t, n) {
    super(
      "missing_refresh_token",
      `Missing Refresh Token (audience: '${bi(t, ["default"])}', scope: '${bi(
        n
      )}')`
    ),
      (this.audience = t),
      (this.scope = n),
      Object.setPrototypeOf(this, Ro.prototype);
  }
}
function bi(e, t = []) {
  return e && !t.includes(e) ? e : "";
}
const no = () => window.crypto,
  Zo = () => {
    const e =
      "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_~.";
    let t = "";
    return (
      Array.from(no().getRandomValues(new Uint8Array(43))).forEach(
        (n) => (t += e[n % e.length])
      ),
      t
    );
  },
  wi = (e) => btoa(e),
  ws = (e) => {
    var { clientId: t } = e,
      n = et(e, ["clientId"]);
    return new URLSearchParams(
      ((o) =>
        Object.keys(o)
          .filter((s) => o[s] !== void 0)
          .reduce(
            (s, r) => Object.assign(Object.assign({}, s), { [r]: o[r] }),
            {}
          ))(Object.assign({ client_id: t }, n))
    ).toString();
  },
  xi = (e) =>
    ((t) =>
      decodeURIComponent(
        atob(t)
          .split("")
          .map((n) => "%" + ("00" + n.charCodeAt(0).toString(16)).slice(-2))
          .join("")
      ))(e.replace(/_/g, "/").replace(/-/g, "+")),
  Td = async (e, t) => {
    const n = await fetch(e, t);
    return { ok: n.ok, json: await n.json() };
  },
  Pd = async (e, t, n, o, s, r, i = 1e4) =>
    s
      ? (async (c, a, l, u, f, d, p) => {
          return (
            (g = {
              auth: { audience: a, scope: l },
              timeout: f,
              fetchUrl: c,
              fetchOptions: u,
              useFormData: p,
            }),
            (y = d),
            new Promise(function (w, x) {
              const v = new MessageChannel();
              (v.port1.onmessage = function (O) {
                O.data.error ? x(new Error(O.data.error)) : w(O.data),
                  v.port1.close();
              }),
                y.postMessage(g, [v.port2]);
            })
          );
          var g, y;
        })(e, t, n, o, i, s, r)
      : (async (c, a, l) => {
          const u = new AbortController();
          let f;
          return (
            (a.signal = u.signal),
            Promise.race([
              Td(c, a),
              new Promise((d, p) => {
                f = setTimeout(() => {
                  u.abort(), p(new Error("Timeout when executing 'fetch'"));
                }, l);
              }),
            ]).finally(() => {
              clearTimeout(f);
            })
          );
        })(e, o, i);
async function Rd(e, t) {
  var {
      baseUrl: n,
      timeout: o,
      audience: s,
      scope: r,
      auth0Client: i,
      useFormData: c,
    } = e,
    a = et(e, [
      "baseUrl",
      "timeout",
      "audience",
      "scope",
      "auth0Client",
      "useFormData",
    ]);
  const l = c ? ws(a) : JSON.stringify(a);
  return await (async function (u, f, d, p, g, y, w) {
    let x,
      v = null;
    for (let T = 0; T < 3; T++)
      try {
        (x = await Pd(u, d, p, g, y, w, f)), (v = null);
        break;
      } catch (Z) {
        v = Z;
      }
    if (v) throw v;
    const O = x.json,
      { error: R, error_description: U } = O,
      F = et(O, ["error", "error_description"]),
      { ok: N } = x;
    if (!N) {
      const T = U || `HTTP error. Unable to fetch ${u}`;
      throw R === "mfa_required"
        ? new ir(R, T, F.mfa_token)
        : R === "missing_refresh_token"
        ? new Ro(d, p)
        : new He(R || "request_error", T);
    }
    return F;
  })(
    `${n}/oauth/token`,
    o,
    s || "default",
    r,
    {
      method: "POST",
      body: l,
      headers: {
        "Content-Type": c
          ? "application/x-www-form-urlencoded"
          : "application/json",
        "Auth0-Client": btoa(JSON.stringify(i || pa)),
      },
    },
    t,
    c
  );
}
const Xn = (...e) => {
  return ((t = e.filter(Boolean).join(" ").trim().split(/\s+/)),
  Array.from(new Set(t))).join(" ");
  var t;
};
class nt {
  constructor(t, n = "@@auth0spajs@@", o) {
    (this.prefix = n),
      (this.suffix = o),
      (this.clientId = t.clientId),
      (this.scope = t.scope),
      (this.audience = t.audience);
  }
  toKey() {
    return [this.prefix, this.clientId, this.audience, this.scope, this.suffix]
      .filter(Boolean)
      .join("::");
  }
  static fromKey(t) {
    const [n, o, s, r] = t.split("::");
    return new nt({ clientId: o, scope: r, audience: s }, n);
  }
  static fromCacheEntry(t) {
    const { scope: n, audience: o, client_id: s } = t;
    return new nt({ scope: n, audience: o, clientId: s });
  }
}
class Ad {
  set(t, n) {
    localStorage.setItem(t, JSON.stringify(n));
  }
  get(t) {
    const n = window.localStorage.getItem(t);
    if (n)
      try {
        return JSON.parse(n);
      } catch {
        return;
      }
  }
  remove(t) {
    localStorage.removeItem(t);
  }
  allKeys() {
    return Object.keys(window.localStorage).filter((t) =>
      t.startsWith("@@auth0spajs@@")
    );
  }
}
class ga {
  constructor() {
    this.enclosedCache = (function () {
      let t = {};
      return {
        set(n, o) {
          t[n] = o;
        },
        get(n) {
          const o = t[n];
          if (o) return o;
        },
        remove(n) {
          delete t[n];
        },
        allKeys: () => Object.keys(t),
      };
    })();
  }
}
class jd {
  constructor(t, n, o) {
    (this.cache = t), (this.keyManifest = n), (this.nowProvider = o || ma);
  }
  async setIdToken(t, n, o) {
    var s;
    const r = this.getIdTokenCacheKey(t);
    await this.cache.set(r, { id_token: n, decodedToken: o }),
      await ((s = this.keyManifest) === null || s === void 0
        ? void 0
        : s.add(r));
  }
  async getIdToken(t) {
    const n = await this.cache.get(this.getIdTokenCacheKey(t.clientId));
    if (!n && t.scope && t.audience) {
      const o = await this.get(t);
      return !o || !o.id_token || !o.decodedToken
        ? void 0
        : { id_token: o.id_token, decodedToken: o.decodedToken };
    }
    if (n) return { id_token: n.id_token, decodedToken: n.decodedToken };
  }
  async get(t, n = 0) {
    var o;
    let s = await this.cache.get(t.toKey());
    if (!s) {
      const c = await this.getCacheKeys();
      if (!c) return;
      const a = this.matchExistingCacheKey(t, c);
      a && (s = await this.cache.get(a));
    }
    if (!s) return;
    const r = await this.nowProvider(),
      i = Math.floor(r / 1e3);
    return s.expiresAt - n < i
      ? s.body.refresh_token
        ? ((s.body = { refresh_token: s.body.refresh_token }),
          await this.cache.set(t.toKey(), s),
          s.body)
        : (await this.cache.remove(t.toKey()),
          void (await ((o = this.keyManifest) === null || o === void 0
            ? void 0
            : o.remove(t.toKey()))))
      : s.body;
  }
  async set(t) {
    var n;
    const o = new nt({
        clientId: t.client_id,
        scope: t.scope,
        audience: t.audience,
      }),
      s = await this.wrapCacheEntry(t);
    await this.cache.set(o.toKey(), s),
      await ((n = this.keyManifest) === null || n === void 0
        ? void 0
        : n.add(o.toKey()));
  }
  async clear(t) {
    var n;
    const o = await this.getCacheKeys();
    o &&
      (await o
        .filter((s) => !t || s.includes(t))
        .reduce(async (s, r) => {
          await s, await this.cache.remove(r);
        }, Promise.resolve()),
      await ((n = this.keyManifest) === null || n === void 0
        ? void 0
        : n.clear()));
  }
  async wrapCacheEntry(t) {
    const n = await this.nowProvider();
    return { body: t, expiresAt: Math.floor(n / 1e3) + t.expires_in };
  }
  async getCacheKeys() {
    var t;
    return this.keyManifest
      ? (t = await this.keyManifest.get()) === null || t === void 0
        ? void 0
        : t.keys
      : this.cache.allKeys
      ? this.cache.allKeys()
      : void 0;
  }
  getIdTokenCacheKey(t) {
    return new nt({ clientId: t }, "@@auth0spajs@@", "@@user@@").toKey();
  }
  matchExistingCacheKey(t, n) {
    return n.filter((o) => {
      var s;
      const r = nt.fromKey(o),
        i = new Set(r.scope && r.scope.split(" ")),
        c =
          ((s = t.scope) === null || s === void 0 ? void 0 : s.split(" ")) ||
          [],
        a = r.scope && c.reduce((l, u) => l && i.has(u), !0);
      return (
        r.prefix === "@@auth0spajs@@" &&
        r.clientId === t.clientId &&
        r.audience === t.audience &&
        a
      );
    })[0];
  }
}
class $d {
  constructor(t, n) {
    (this.storage = t),
      (this.clientId = n),
      (this.storageKey = `a0.spajs.txs.${this.clientId}`),
      (this.transaction = this.storage.get(this.storageKey));
  }
  create(t) {
    (this.transaction = t),
      this.storage.save(this.storageKey, t, { daysUntilExpire: 1 });
  }
  get() {
    return this.transaction;
  }
  remove() {
    delete this.transaction, this.storage.remove(this.storageKey);
  }
}
const pn = (e) => typeof e == "number",
  Ld = [
    "iss",
    "aud",
    "exp",
    "nbf",
    "iat",
    "jti",
    "azp",
    "nonce",
    "auth_time",
    "at_hash",
    "c_hash",
    "acr",
    "amr",
    "sub_jwk",
    "cnf",
    "sip_from_tag",
    "sip_date",
    "sip_callid",
    "sip_cseq_num",
    "sip_via_branch",
    "orig",
    "dest",
    "mky",
    "events",
    "toe",
    "txn",
    "rph",
    "sid",
    "vot",
    "vtm",
  ];
var Dt = nr(function (e, t) {
  var n =
    (Yt && Yt.__assign) ||
    function () {
      return (
        (n =
          Object.assign ||
          function (a) {
            for (var l, u = 1, f = arguments.length; u < f; u++)
              for (var d in (l = arguments[u]))
                Object.prototype.hasOwnProperty.call(l, d) && (a[d] = l[d]);
            return a;
          }),
        n.apply(this, arguments)
      );
    };
  function o(a, l) {
    if (!l) return "";
    var u = "; " + a;
    return l === !0 ? u : u + "=" + l;
  }
  function s(a, l, u) {
    return (
      encodeURIComponent(a)
        .replace(/%(23|24|26|2B|5E|60|7C)/g, decodeURIComponent)
        .replace(/\(/g, "%28")
        .replace(/\)/g, "%29") +
      "=" +
      encodeURIComponent(l).replace(
        /%(23|24|26|2B|3A|3C|3E|3D|2F|3F|40|5B|5D|5E|60|7B|7D|7C)/g,
        decodeURIComponent
      ) +
      (function (f) {
        if (typeof f.expires == "number") {
          var d = new Date();
          d.setMilliseconds(d.getMilliseconds() + 864e5 * f.expires),
            (f.expires = d);
        }
        return (
          o("Expires", f.expires ? f.expires.toUTCString() : "") +
          o("Domain", f.domain) +
          o("Path", f.path) +
          o("Secure", f.secure) +
          o("SameSite", f.sameSite)
        );
      })(u)
    );
  }
  function r(a) {
    for (
      var l = {}, u = a ? a.split("; ") : [], f = /(%[\dA-F]{2})+/gi, d = 0;
      d < u.length;
      d++
    ) {
      var p = u[d].split("="),
        g = p.slice(1).join("=");
      g.charAt(0) === '"' && (g = g.slice(1, -1));
      try {
        l[p[0].replace(f, decodeURIComponent)] = g.replace(
          f,
          decodeURIComponent
        );
      } catch {}
    }
    return l;
  }
  function i() {
    return r(document.cookie);
  }
  function c(a, l, u) {
    document.cookie = s(a, l, n({ path: "/" }, u));
  }
  (t.__esModule = !0),
    (t.encode = s),
    (t.parse = r),
    (t.getAll = i),
    (t.get = function (a) {
      return i()[a];
    }),
    (t.set = c),
    (t.remove = function (a, l) {
      c(a, "", n(n({}, l), { expires: -1 }));
    });
});
tr(Dt), Dt.encode, Dt.parse, Dt.getAll;
var Nd = Dt.get,
  _a = Dt.set,
  ya = Dt.remove;
const Gt = {
    get(e) {
      const t = Nd(e);
      if (t !== void 0) return JSON.parse(t);
    },
    save(e, t, n) {
      let o = {};
      window.location.protocol === "https:" &&
        (o = { secure: !0, sameSite: "none" }),
        n != null && n.daysUntilExpire && (o.expires = n.daysUntilExpire),
        n != null && n.cookieDomain && (o.domain = n.cookieDomain),
        _a(e, JSON.stringify(t), o);
    },
    remove(e, t) {
      let n = {};
      t != null && t.cookieDomain && (n.domain = t.cookieDomain), ya(e, n);
    },
  },
  Md = {
    get: (e) => Gt.get(e) || Gt.get(`_legacy_${e}`),
    save(e, t, n) {
      let o = {};
      window.location.protocol === "https:" && (o = { secure: !0 }),
        n != null && n.daysUntilExpire && (o.expires = n.daysUntilExpire),
        n != null && n.cookieDomain && (o.domain = n.cookieDomain),
        _a(`_legacy_${e}`, JSON.stringify(t), o),
        Gt.save(e, t, n);
    },
    remove(e, t) {
      let n = {};
      t != null && t.cookieDomain && (n.domain = t.cookieDomain),
        ya(e, n),
        Gt.remove(e, t),
        Gt.remove(`_legacy_${e}`, t);
    },
  },
  Fd = {
    get(e) {
      if (typeof sessionStorage > "u") return;
      const t = sessionStorage.getItem(e);
      return t != null ? JSON.parse(t) : void 0;
    },
    save(e, t) {
      sessionStorage.setItem(e, JSON.stringify(t));
    },
    remove(e) {
      sessionStorage.removeItem(e);
    },
  };
var qo,
  Dd = function (e) {
    return (
      (qo =
        qo ||
        (function (t, n, o) {
          var s = n === void 0 ? null : n,
            r = (function (l, u) {
              var f = atob(l);
              if (u) {
                for (
                  var d = new Uint8Array(f.length), p = 0, g = f.length;
                  p < g;
                  ++p
                )
                  d[p] = f.charCodeAt(p);
                return String.fromCharCode.apply(
                  null,
                  new Uint16Array(d.buffer)
                );
              }
              return f;
            })(t, o !== void 0 && o),
            i =
              r.indexOf(
                `
`,
                10
              ) + 1,
            c = r.substring(i) + (s ? "//# sourceMappingURL=" + s : ""),
            a = new Blob([c], { type: "application/javascript" });
          return URL.createObjectURL(a);
        })(
          "Lyogcm9sbHVwLXBsdWdpbi13ZWItd29ya2VyLWxvYWRlciAqLwohZnVuY3Rpb24oKXsidXNlIHN0cmljdCI7Y2xhc3MgZSBleHRlbmRzIEVycm9ye2NvbnN0cnVjdG9yKHQscil7c3VwZXIociksdGhpcy5lcnJvcj10LHRoaXMuZXJyb3JfZGVzY3JpcHRpb249cixPYmplY3Quc2V0UHJvdG90eXBlT2YodGhpcyxlLnByb3RvdHlwZSl9c3RhdGljIGZyb21QYXlsb2FkKHtlcnJvcjp0LGVycm9yX2Rlc2NyaXB0aW9uOnJ9KXtyZXR1cm4gbmV3IGUodCxyKX19Y2xhc3MgdCBleHRlbmRzIGV7Y29uc3RydWN0b3IoZSxzKXtzdXBlcigibWlzc2luZ19yZWZyZXNoX3Rva2VuIixgTWlzc2luZyBSZWZyZXNoIFRva2VuIChhdWRpZW5jZTogJyR7cihlLFsiZGVmYXVsdCJdKX0nLCBzY29wZTogJyR7cihzKX0nKWApLHRoaXMuYXVkaWVuY2U9ZSx0aGlzLnNjb3BlPXMsT2JqZWN0LnNldFByb3RvdHlwZU9mKHRoaXMsdC5wcm90b3R5cGUpfX1mdW5jdGlvbiByKGUsdD1bXSl7cmV0dXJuIGUmJiF0LmluY2x1ZGVzKGUpP2U6IiJ9Y29uc3Qgcz1lPT57dmFye2NsaWVudElkOnR9PWUscj1mdW5jdGlvbihlLHQpe3ZhciByPXt9O2Zvcih2YXIgcyBpbiBlKU9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbChlLHMpJiZ0LmluZGV4T2Yocyk8MCYmKHJbc109ZVtzXSk7aWYobnVsbCE9ZSYmImZ1bmN0aW9uIj09dHlwZW9mIE9iamVjdC5nZXRPd25Qcm9wZXJ0eVN5bWJvbHMpe3ZhciBvPTA7Zm9yKHM9T2JqZWN0LmdldE93blByb3BlcnR5U3ltYm9scyhlKTtvPHMubGVuZ3RoO28rKyl0LmluZGV4T2Yoc1tvXSk8MCYmT2JqZWN0LnByb3RvdHlwZS5wcm9wZXJ0eUlzRW51bWVyYWJsZS5jYWxsKGUsc1tvXSkmJihyW3Nbb11dPWVbc1tvXV0pfXJldHVybiByfShlLFsiY2xpZW50SWQiXSk7cmV0dXJuIG5ldyBVUkxTZWFyY2hQYXJhbXMoKGU9Pk9iamVjdC5rZXlzKGUpLmZpbHRlcigodD0+dm9pZCAwIT09ZVt0XSkpLnJlZHVjZSgoKHQscik9Pk9iamVjdC5hc3NpZ24oT2JqZWN0LmFzc2lnbih7fSx0KSx7W3JdOmVbcl19KSkse30pKShPYmplY3QuYXNzaWduKHtjbGllbnRfaWQ6dH0scikpKS50b1N0cmluZygpfTtsZXQgbz17fTtjb25zdCBuPShlLHQpPT5gJHtlfXwke3R9YDthZGRFdmVudExpc3RlbmVyKCJtZXNzYWdlIiwoYXN5bmMoe2RhdGE6e3RpbWVvdXQ6ZSxhdXRoOnIsZmV0Y2hVcmw6aSxmZXRjaE9wdGlvbnM6Yyx1c2VGb3JtRGF0YTphfSxwb3J0czpbZl19KT0+e2xldCBwO2NvbnN0e2F1ZGllbmNlOmwsc2NvcGU6dX09cnx8e307dHJ5e2NvbnN0IHI9YT8oZT0+e2NvbnN0IHQ9bmV3IFVSTFNlYXJjaFBhcmFtcyhlKSxyPXt9O3JldHVybiB0LmZvckVhY2goKChlLHQpPT57clt0XT1lfSkpLHJ9KShjLmJvZHkpOkpTT04ucGFyc2UoYy5ib2R5KTtpZighci5yZWZyZXNoX3Rva2VuJiYicmVmcmVzaF90b2tlbiI9PT1yLmdyYW50X3R5cGUpe2NvbnN0IGU9KChlLHQpPT5vW24oZSx0KV0pKGwsdSk7aWYoIWUpdGhyb3cgbmV3IHQobCx1KTtjLmJvZHk9YT9zKE9iamVjdC5hc3NpZ24oT2JqZWN0LmFzc2lnbih7fSxyKSx7cmVmcmVzaF90b2tlbjplfSkpOkpTT04uc3RyaW5naWZ5KE9iamVjdC5hc3NpZ24oT2JqZWN0LmFzc2lnbih7fSxyKSx7cmVmcmVzaF90b2tlbjplfSkpfWxldCBkLGc7ImZ1bmN0aW9uIj09dHlwZW9mIEFib3J0Q29udHJvbGxlciYmKGQ9bmV3IEFib3J0Q29udHJvbGxlcixjLnNpZ25hbD1kLnNpZ25hbCk7dHJ5e2c9YXdhaXQgUHJvbWlzZS5yYWNlKFsoaD1lLG5ldyBQcm9taXNlKChlPT5zZXRUaW1lb3V0KGUsaCkpKSksZmV0Y2goaSxPYmplY3QuYXNzaWduKHt9LGMpKV0pfWNhdGNoKGUpe3JldHVybiB2b2lkIGYucG9zdE1lc3NhZ2Uoe2Vycm9yOmUubWVzc2FnZX0pfWlmKCFnKXJldHVybiBkJiZkLmFib3J0KCksdm9pZCBmLnBvc3RNZXNzYWdlKHtlcnJvcjoiVGltZW91dCB3aGVuIGV4ZWN1dGluZyAnZmV0Y2gnIn0pO3A9YXdhaXQgZy5qc29uKCkscC5yZWZyZXNoX3Rva2VuPygoKGUsdCxyKT0+e29bbih0LHIpXT1lfSkocC5yZWZyZXNoX3Rva2VuLGwsdSksZGVsZXRlIHAucmVmcmVzaF90b2tlbik6KChlLHQpPT57ZGVsZXRlIG9bbihlLHQpXX0pKGwsdSksZi5wb3N0TWVzc2FnZSh7b2s6Zy5vayxqc29uOnB9KX1jYXRjaChlKXtmLnBvc3RNZXNzYWdlKHtvazohMSxqc29uOntlcnJvcjplLmVycm9yLGVycm9yX2Rlc2NyaXB0aW9uOmUubWVzc2FnZX19KX12YXIgaH0pKX0oKTsKCg==",
          null,
          !1
        )),
      new Worker(qo, e)
    );
  };
const Xo = {};
class Ud {
  constructor(t, n) {
    (this.cache = t),
      (this.clientId = n),
      (this.manifestKey = this.createManifestKeyFrom(this.clientId));
  }
  async add(t) {
    var n;
    const o = new Set(
      ((n = await this.cache.get(this.manifestKey)) === null || n === void 0
        ? void 0
        : n.keys) || []
    );
    o.add(t), await this.cache.set(this.manifestKey, { keys: [...o] });
  }
  async remove(t) {
    const n = await this.cache.get(this.manifestKey);
    if (n) {
      const o = new Set(n.keys);
      return (
        o.delete(t),
        o.size > 0
          ? await this.cache.set(this.manifestKey, { keys: [...o] })
          : await this.cache.remove(this.manifestKey)
      );
    }
  }
  get() {
    return this.cache.get(this.manifestKey);
  }
  clear() {
    return this.cache.remove(this.manifestKey);
  }
  createManifestKeyFrom(t) {
    return `@@auth0spajs@@::${t}`;
  }
}
const zd = {
    memory: () => new ga().enclosedCache,
    localstorage: () => new Ad(),
  },
  ki = (e) => zd[e],
  Ci = (e) => {
    const { openUrl: t, onRedirect: n } = e,
      o = et(e, ["openUrl", "onRedirect"]);
    return Object.assign(Object.assign({}, o), {
      openUrl: t === !1 || t ? t : n,
    });
  },
  Jo = new Ed();
class Kd {
  constructor(t) {
    let n, o;
    if (
      ((this.userCache = new ga().enclosedCache),
      (this.defaultOptions = {
        authorizationParams: { scope: "openid profile email" },
        useRefreshTokensFallback: !1,
        useFormData: !0,
      }),
      (this._releaseLockOnPageHide = async () => {
        await Jo.releaseLock("auth0.lock.getTokenSilently"),
          window.removeEventListener("pagehide", this._releaseLockOnPageHide);
      }),
      (this.options = Object.assign(
        Object.assign(Object.assign({}, this.defaultOptions), t),
        {
          authorizationParams: Object.assign(
            Object.assign({}, this.defaultOptions.authorizationParams),
            t.authorizationParams
          ),
        }
      )),
      typeof window < "u" &&
        (() => {
          if (!no())
            throw new Error(
              "For security reasons, `window.crypto` is required to run `auth0-spa-js`."
            );
          if (no().subtle === void 0)
            throw new Error(`
      auth0-spa-js must run on a secure origin. See https://github.com/auth0/auth0-spa-js/blob/master/FAQ.md#why-do-i-get-auth0-spa-js-must-run-on-a-secure-origin for more information.
    `);
        })(),
      t.cache &&
        t.cacheLocation &&
        console.warn(
          "Both `cache` and `cacheLocation` options have been specified in the Auth0Client configuration; ignoring `cacheLocation` and using `cache`."
        ),
      t.cache)
    )
      o = t.cache;
    else {
      if (((n = t.cacheLocation || "memory"), !ki(n)))
        throw new Error(`Invalid cache location "${n}"`);
      o = ki(n)();
    }
    (this.httpTimeoutMs = t.httpTimeoutInSeconds
      ? 1e3 * t.httpTimeoutInSeconds
      : 1e4),
      (this.cookieStorage = t.legacySameSiteCookie === !1 ? Gt : Md),
      (this.orgHintCookieName = `auth0.${this.options.clientId}.organization_hint`),
      (this.isAuthenticatedCookieName = ((i) =>
        `auth0.${this.options.clientId}.is.authenticated`)()),
      (this.sessionCheckExpiryDays = t.sessionCheckExpiryDays || 1);
    const s = t.useCookiesForTransactions ? this.cookieStorage : Fd;
    var r;
    (this.scope = Xn(
      "openid",
      this.options.authorizationParams.scope,
      this.options.useRefreshTokens ? "offline_access" : ""
    )),
      (this.transactionManager = new $d(s, this.options.clientId)),
      (this.nowProvider = this.options.nowProvider || ma),
      (this.cacheManager = new jd(
        o,
        o.allKeys ? void 0 : new Ud(o, this.options.clientId),
        this.nowProvider
      )),
      (this.domainUrl =
        ((r = this.options.domain),
        /^https?:\/\//.test(r) ? r : `https://${r}`)),
      (this.tokenIssuer = ((i, c) =>
        i ? (i.startsWith("https://") ? i : `https://${i}/`) : `${c}/`)(
        this.options.issuer,
        this.domainUrl
      )),
      typeof window < "u" &&
        window.Worker &&
        this.options.useRefreshTokens &&
        n === "memory" &&
        (this.worker = new Dd());
  }
  _url(t) {
    const n = encodeURIComponent(
      btoa(JSON.stringify(this.options.auth0Client || pa))
    );
    return `${this.domainUrl}${t}&auth0Client=${n}`;
  }
  _authorizeUrl(t) {
    return this._url(`/authorize?${ws(t)}`);
  }
  async _verifyIdToken(t, n, o) {
    const s = await this.nowProvider();
    return ((i) => {
      if (!i.id_token) throw new Error("ID token is required but missing");
      const c = ((f) => {
        const d = f.split("."),
          [p, g, y] = d;
        if (d.length !== 3 || !p || !g || !y)
          throw new Error("ID token could not be decoded");
        const w = JSON.parse(xi(g)),
          x = { __raw: f },
          v = {};
        return (
          Object.keys(w).forEach((O) => {
            (x[O] = w[O]), Ld.includes(O) || (v[O] = w[O]);
          }),
          {
            encoded: { header: p, payload: g, signature: y },
            header: JSON.parse(xi(p)),
            claims: x,
            user: v,
          }
        );
      })(i.id_token);
      if (!c.claims.iss)
        throw new Error(
          "Issuer (iss) claim must be a string present in the ID token"
        );
      if (c.claims.iss !== i.iss)
        throw new Error(
          `Issuer (iss) claim mismatch in the ID token; expected "${i.iss}", found "${c.claims.iss}"`
        );
      if (!c.user.sub)
        throw new Error(
          "Subject (sub) claim must be a string present in the ID token"
        );
      if (c.header.alg !== "RS256")
        throw new Error(
          `Signature algorithm of "${c.header.alg}" is not supported. Expected the ID token to be signed with "RS256".`
        );
      if (
        !c.claims.aud ||
        (typeof c.claims.aud != "string" && !Array.isArray(c.claims.aud))
      )
        throw new Error(
          "Audience (aud) claim must be a string or array of strings present in the ID token"
        );
      if (Array.isArray(c.claims.aud)) {
        if (!c.claims.aud.includes(i.aud))
          throw new Error(
            `Audience (aud) claim mismatch in the ID token; expected "${
              i.aud
            }" but was not one of "${c.claims.aud.join(", ")}"`
          );
        if (c.claims.aud.length > 1) {
          if (!c.claims.azp)
            throw new Error(
              "Authorized Party (azp) claim must be a string present in the ID token when Audience (aud) claim has multiple values"
            );
          if (c.claims.azp !== i.aud)
            throw new Error(
              `Authorized Party (azp) claim mismatch in the ID token; expected "${i.aud}", found "${c.claims.azp}"`
            );
        }
      } else if (c.claims.aud !== i.aud)
        throw new Error(
          `Audience (aud) claim mismatch in the ID token; expected "${i.aud}" but found "${c.claims.aud}"`
        );
      if (i.nonce) {
        if (!c.claims.nonce)
          throw new Error(
            "Nonce (nonce) claim must be a string present in the ID token"
          );
        if (c.claims.nonce !== i.nonce)
          throw new Error(
            `Nonce (nonce) claim mismatch in the ID token; expected "${i.nonce}", found "${c.claims.nonce}"`
          );
      }
      if (i.max_age && !pn(c.claims.auth_time))
        throw new Error(
          "Authentication Time (auth_time) claim must be a number present in the ID token when Max Age (max_age) is specified"
        );
      if (c.claims.exp == null || !pn(c.claims.exp))
        throw new Error(
          "Expiration Time (exp) claim must be a number present in the ID token"
        );
      if (!pn(c.claims.iat))
        throw new Error(
          "Issued At (iat) claim must be a number present in the ID token"
        );
      const a = i.leeway || 60,
        l = new Date(i.now || Date.now()),
        u = new Date(0);
      if ((u.setUTCSeconds(c.claims.exp + a), l > u))
        throw new Error(
          `Expiration Time (exp) claim error in the ID token; current time (${l}) is after expiration time (${u})`
        );
      if (c.claims.nbf != null && pn(c.claims.nbf)) {
        const f = new Date(0);
        if ((f.setUTCSeconds(c.claims.nbf - a), l < f))
          throw new Error(
            `Not Before time (nbf) claim in the ID token indicates that this token can't be used just yet. Current time (${l}) is before ${f}`
          );
      }
      if (c.claims.auth_time != null && pn(c.claims.auth_time)) {
        const f = new Date(0);
        if (
          (f.setUTCSeconds(parseInt(c.claims.auth_time) + i.max_age + a), l > f)
        )
          throw new Error(
            `Authentication Time (auth_time) claim in the ID token indicates that too much time has passed since the last end-user authentication. Current time (${l}) is after last auth at ${f}`
          );
      }
      if (i.organizationId) {
        if (!c.claims.org_id)
          throw new Error(
            "Organization ID (org_id) claim must be a string present in the ID token"
          );
        if (i.organizationId !== c.claims.org_id)
          throw new Error(
            `Organization ID (org_id) claim mismatch in the ID token; expected "${i.organizationId}", found "${c.claims.org_id}"`
          );
      }
      return c;
    })({
      iss: this.tokenIssuer,
      aud: this.options.clientId,
      id_token: t,
      nonce: n,
      organizationId: o,
      leeway: this.options.leeway,
      max_age:
        ((r = this.options.authorizationParams.max_age),
        typeof r != "string" ? r : parseInt(r, 10) || void 0),
      now: s,
    });
    var r;
  }
  _processOrgIdHint(t) {
    t
      ? this.cookieStorage.save(this.orgHintCookieName, t, {
          daysUntilExpire: this.sessionCheckExpiryDays,
          cookieDomain: this.options.cookieDomain,
        })
      : this.cookieStorage.remove(this.orgHintCookieName, {
          cookieDomain: this.options.cookieDomain,
        });
  }
  async _prepareAuthorizeUrl(t, n, o) {
    const s = wi(Zo()),
      r = wi(Zo()),
      i = Zo(),
      c = ((u) => {
        const f = new Uint8Array(u);
        return ((d) => {
          const p = { "+": "-", "/": "_", "=": "" };
          return d.replace(/[+/=]/g, (g) => p[g]);
        })(window.btoa(String.fromCharCode(...Array.from(f))));
      })(
        await (async (u) =>
          await no().subtle.digest(
            { name: "SHA-256" },
            new TextEncoder().encode(u)
          ))(i)
      ),
      a = ((u, f, d, p, g, y, w, x) =>
        Object.assign(
          Object.assign(
            Object.assign({ client_id: u.clientId }, u.authorizationParams),
            d
          ),
          {
            scope: Xn(f, d.scope),
            response_type: "code",
            response_mode: x || "query",
            state: p,
            nonce: g,
            redirect_uri: w || u.authorizationParams.redirect_uri,
            code_challenge: y,
            code_challenge_method: "S256",
          }
        ))(
        this.options,
        this.scope,
        t,
        s,
        r,
        c,
        t.redirect_uri || this.options.authorizationParams.redirect_uri || o,
        n == null ? void 0 : n.response_mode
      ),
      l = this._authorizeUrl(a);
    return {
      nonce: r,
      code_verifier: i,
      scope: a.scope,
      audience: a.audience || "default",
      redirect_uri: a.redirect_uri,
      state: s,
      url: l,
    };
  }
  async loginWithPopup(t, n) {
    var o;
    if (
      ((t = t || {}),
      !(n = n || {}).popup &&
        ((n.popup = ((c) => {
          const a = window.screenX + (window.innerWidth - 400) / 2,
            l = window.screenY + (window.innerHeight - 600) / 2;
          return window.open(
            "",
            "auth0:authorize:popup",
            `left=${a},top=${l},width=400,height=600,resizable,scrollbars=yes,status=1`
          );
        })()),
        !n.popup))
    )
      throw new Error(
        "Unable to open a popup for loginWithPopup - window.open returned `null`"
      );
    const s = await this._prepareAuthorizeUrl(
      t.authorizationParams || {},
      { response_mode: "web_message" },
      window.location.origin
    );
    n.popup.location.href = s.url;
    const r = await ((c) =>
      new Promise((a, l) => {
        let u;
        const f = setInterval(() => {
            c.popup &&
              c.popup.closed &&
              (clearInterval(f),
              clearTimeout(d),
              window.removeEventListener("message", u, !1),
              l(new rr(c.popup)));
          }, 1e3),
          d = setTimeout(() => {
            clearInterval(f),
              l(new sr(c.popup)),
              window.removeEventListener("message", u, !1);
          }, 1e3 * (c.timeoutInSeconds || 60));
        (u = function (p) {
          if (p.data && p.data.type === "authorization_response") {
            if (
              (clearTimeout(d),
              clearInterval(f),
              window.removeEventListener("message", u, !1),
              c.popup.close(),
              p.data.response.error)
            )
              return l(He.fromPayload(p.data.response));
            a(p.data.response);
          }
        }),
          window.addEventListener("message", u);
      }))(
      Object.assign(Object.assign({}, n), {
        timeoutInSeconds:
          n.timeoutInSeconds || this.options.authorizeTimeoutInSeconds || 60,
      })
    );
    if (s.state !== r.state) throw new Error("Invalid state");
    const i =
      ((o = t.authorizationParams) === null || o === void 0
        ? void 0
        : o.organization) || this.options.authorizationParams.organization;
    await this._requestToken(
      {
        audience: s.audience,
        scope: s.scope,
        code_verifier: s.code_verifier,
        grant_type: "authorization_code",
        code: r.code,
        redirect_uri: s.redirect_uri,
      },
      { nonceIn: s.nonce, organizationId: i }
    );
  }
  async getUser() {
    var t;
    const n = await this._getIdTokenFromCache();
    return (t = n == null ? void 0 : n.decodedToken) === null || t === void 0
      ? void 0
      : t.user;
  }
  async getIdTokenClaims() {
    var t;
    const n = await this._getIdTokenFromCache();
    return (t = n == null ? void 0 : n.decodedToken) === null || t === void 0
      ? void 0
      : t.claims;
  }
  async loginWithRedirect(t = {}) {
    var n;
    const o = Ci(t),
      { openUrl: s, fragment: r, appState: i } = o,
      c = et(o, ["openUrl", "fragment", "appState"]),
      a =
        ((n = c.authorizationParams) === null || n === void 0
          ? void 0
          : n.organization) || this.options.authorizationParams.organization,
      l = await this._prepareAuthorizeUrl(c.authorizationParams || {}),
      { url: u } = l,
      f = et(l, ["url"]);
    this.transactionManager.create(
      Object.assign(
        Object.assign(Object.assign({}, f), { appState: i }),
        a && { organizationId: a }
      )
    );
    const d = r ? `${u}#${r}` : u;
    s ? await s(d) : window.location.assign(d);
  }
  async handleRedirectCallback(t = window.location.href) {
    const n = t.split("?").slice(1);
    if (n.length === 0)
      throw new Error("There are no query params available for parsing.");
    const {
        state: o,
        code: s,
        error: r,
        error_description: i,
      } = ((f) => {
        f.indexOf("#") > -1 && (f = f.substring(0, f.indexOf("#")));
        const d = new URLSearchParams(f);
        return {
          state: d.get("state"),
          code: d.get("code") || void 0,
          error: d.get("error") || void 0,
          error_description: d.get("error_description") || void 0,
        };
      })(n.join("")),
      c = this.transactionManager.get();
    if (!c) throw new Error("Invalid state");
    if ((this.transactionManager.remove(), r))
      throw new or(r, i || r, o, c.appState);
    if (!c.code_verifier || (c.state && c.state !== o))
      throw new Error("Invalid state");
    const a = c.organizationId,
      l = c.nonce,
      u = c.redirect_uri;
    return (
      await this._requestToken(
        Object.assign(
          {
            audience: c.audience,
            scope: c.scope,
            code_verifier: c.code_verifier,
            grant_type: "authorization_code",
            code: s,
          },
          u ? { redirect_uri: u } : {}
        ),
        { nonceIn: l, organizationId: a }
      ),
      { appState: c.appState }
    );
  }
  async checkSession(t) {
    if (!this.cookieStorage.get(this.isAuthenticatedCookieName)) {
      if (!this.cookieStorage.get("auth0.is.authenticated")) return;
      this.cookieStorage.save(this.isAuthenticatedCookieName, !0, {
        daysUntilExpire: this.sessionCheckExpiryDays,
        cookieDomain: this.options.cookieDomain,
      }),
        this.cookieStorage.remove("auth0.is.authenticated");
    }
    try {
      await this.getTokenSilently(t);
    } catch {}
  }
  async getTokenSilently(t = {}) {
    var n;
    const o = Object.assign(Object.assign({ cacheMode: "on" }, t), {
        authorizationParams: Object.assign(
          Object.assign(
            Object.assign({}, this.options.authorizationParams),
            t.authorizationParams
          ),
          {
            scope: Xn(
              this.scope,
              (n = t.authorizationParams) === null || n === void 0
                ? void 0
                : n.scope
            ),
          }
        ),
      }),
      s = await ((r, i) => {
        let c = Xo[i];
        return (
          c ||
            ((c = r().finally(() => {
              delete Xo[i], (c = null);
            })),
            (Xo[i] = c)),
          c
        );
      })(
        () => this._getTokenSilently(o),
        `${this.options.clientId}::${o.authorizationParams.audience}::${o.authorizationParams.scope}`
      );
    return t.detailedResponse ? s : s == null ? void 0 : s.access_token;
  }
  async _getTokenSilently(t) {
    const { cacheMode: n } = t,
      o = et(t, ["cacheMode"]);
    if (n !== "off") {
      const s = await this._getEntryFromCache({
        scope: o.authorizationParams.scope,
        audience: o.authorizationParams.audience || "default",
        clientId: this.options.clientId,
      });
      if (s) return s;
    }
    if (n !== "cache-only") {
      if (
        !(await (async (s, r = 3) => {
          for (let i = 0; i < r; i++) if (await s()) return !0;
          return !1;
        })(() => Jo.acquireLock("auth0.lock.getTokenSilently", 5e3), 10))
      )
        throw new Mn();
      try {
        if (
          (window.addEventListener("pagehide", this._releaseLockOnPageHide),
          n !== "off")
        ) {
          const l = await this._getEntryFromCache({
            scope: o.authorizationParams.scope,
            audience: o.authorizationParams.audience || "default",
            clientId: this.options.clientId,
          });
          if (l) return l;
        }
        const s = this.options.useRefreshTokens
            ? await this._getTokenUsingRefreshToken(o)
            : await this._getTokenFromIFrame(o),
          {
            id_token: r,
            access_token: i,
            oauthTokenScope: c,
            expires_in: a,
          } = s;
        return Object.assign(
          Object.assign(
            { id_token: r, access_token: i },
            c ? { scope: c } : null
          ),
          { expires_in: a }
        );
      } finally {
        await Jo.releaseLock("auth0.lock.getTokenSilently"),
          window.removeEventListener("pagehide", this._releaseLockOnPageHide);
      }
    }
  }
  async getTokenWithPopup(t = {}, n = {}) {
    var o;
    const s = Object.assign(Object.assign({}, t), {
      authorizationParams: Object.assign(
        Object.assign(
          Object.assign({}, this.options.authorizationParams),
          t.authorizationParams
        ),
        {
          scope: Xn(
            this.scope,
            (o = t.authorizationParams) === null || o === void 0
              ? void 0
              : o.scope
          ),
        }
      ),
    });
    return (
      (n = Object.assign(Object.assign({}, Od), n)),
      await this.loginWithPopup(s, n),
      (
        await this.cacheManager.get(
          new nt({
            scope: s.authorizationParams.scope,
            audience: s.authorizationParams.audience || "default",
            clientId: this.options.clientId,
          })
        )
      ).access_token
    );
  }
  async isAuthenticated() {
    return !!(await this.getUser());
  }
  _buildLogoutUrl(t) {
    t.clientId !== null
      ? (t.clientId = t.clientId || this.options.clientId)
      : delete t.clientId;
    const n = t.logoutParams || {},
      { federated: o } = n,
      s = et(n, ["federated"]),
      r = o ? "&federated" : "";
    return (
      this._url(
        `/v2/logout?${ws(Object.assign({ clientId: t.clientId }, s))}`
      ) + r
    );
  }
  async logout(t = {}) {
    const n = Ci(t),
      { openUrl: o } = n,
      s = et(n, ["openUrl"]);
    t.clientId === null
      ? await this.cacheManager.clear()
      : await this.cacheManager.clear(t.clientId || this.options.clientId),
      this.cookieStorage.remove(this.orgHintCookieName, {
        cookieDomain: this.options.cookieDomain,
      }),
      this.cookieStorage.remove(this.isAuthenticatedCookieName, {
        cookieDomain: this.options.cookieDomain,
      }),
      this.userCache.remove("@@user@@");
    const r = this._buildLogoutUrl(s);
    o ? await o(r) : o !== !1 && window.location.assign(r);
  }
  async _getTokenFromIFrame(t) {
    const n = Object.assign(Object.assign({}, t.authorizationParams), {
        prompt: "none",
      }),
      o = this.cookieStorage.get(this.orgHintCookieName);
    o && !n.organization && (n.organization = o);
    const {
      url: s,
      state: r,
      nonce: i,
      code_verifier: c,
      redirect_uri: a,
      scope: l,
      audience: u,
    } = await this._prepareAuthorizeUrl(
      n,
      { response_mode: "web_message" },
      window.location.origin
    );
    try {
      if (window.crossOriginIsolated)
        throw new He(
          "login_required",
          "The application is running in a Cross-Origin Isolated context, silently retrieving a token without refresh token is not possible."
        );
      const f = t.timeoutInSeconds || this.options.authorizeTimeoutInSeconds,
        d = await ((g, y, w = 60) =>
          new Promise((x, v) => {
            const O = window.document.createElement("iframe");
            O.setAttribute("width", "0"),
              O.setAttribute("height", "0"),
              (O.style.display = "none");
            const R = () => {
              window.document.body.contains(O) &&
                (window.document.body.removeChild(O),
                window.removeEventListener("message", U, !1));
            };
            let U;
            const F = setTimeout(() => {
              v(new Mn()), R();
            }, 1e3 * w);
            (U = function (N) {
              if (
                N.origin != y ||
                !N.data ||
                N.data.type !== "authorization_response"
              )
                return;
              const T = N.source;
              T && T.close(),
                N.data.response.error
                  ? v(He.fromPayload(N.data.response))
                  : x(N.data.response),
                clearTimeout(F),
                window.removeEventListener("message", U, !1),
                setTimeout(R, 2e3);
            }),
              window.addEventListener("message", U, !1),
              window.document.body.appendChild(O),
              O.setAttribute("src", g);
          }))(s, this.domainUrl, f);
      if (r !== d.state) throw new Error("Invalid state");
      const p = await this._requestToken(
        Object.assign(Object.assign({}, t.authorizationParams), {
          code_verifier: c,
          code: d.code,
          grant_type: "authorization_code",
          redirect_uri: a,
          timeout: t.authorizationParams.timeout || this.httpTimeoutMs,
        }),
        { nonceIn: i }
      );
      return Object.assign(Object.assign({}, p), {
        scope: l,
        oauthTokenScope: p.scope,
        audience: u,
      });
    } catch (f) {
      throw (f.error === "login_required" && this.logout({ openUrl: !1 }), f);
    }
  }
  async _getTokenUsingRefreshToken(t) {
    const n = await this.cacheManager.get(
      new nt({
        scope: t.authorizationParams.scope,
        audience: t.authorizationParams.audience || "default",
        clientId: this.options.clientId,
      })
    );
    if (!((n && n.refresh_token) || this.worker)) {
      if (this.options.useRefreshTokensFallback)
        return await this._getTokenFromIFrame(t);
      throw new Ro(
        t.authorizationParams.audience || "default",
        t.authorizationParams.scope
      );
    }
    const o =
        t.authorizationParams.redirect_uri ||
        this.options.authorizationParams.redirect_uri ||
        window.location.origin,
      s =
        typeof t.timeoutInSeconds == "number" ? 1e3 * t.timeoutInSeconds : null;
    try {
      const r = await this._requestToken(
        Object.assign(
          Object.assign(Object.assign({}, t.authorizationParams), {
            grant_type: "refresh_token",
            refresh_token: n && n.refresh_token,
            redirect_uri: o,
          }),
          s && { timeout: s }
        )
      );
      return Object.assign(Object.assign({}, r), {
        scope: t.authorizationParams.scope,
        oauthTokenScope: r.scope,
        audience: t.authorizationParams.audience || "default",
      });
    } catch (r) {
      if (
        (r.message.indexOf("Missing Refresh Token") > -1 ||
          (r.message && r.message.indexOf("invalid refresh token") > -1)) &&
        this.options.useRefreshTokensFallback
      )
        return await this._getTokenFromIFrame(t);
      throw r;
    }
  }
  async _saveEntryInCache(t) {
    const { id_token: n, decodedToken: o } = t,
      s = et(t, ["id_token", "decodedToken"]);
    this.userCache.set("@@user@@", { id_token: n, decodedToken: o }),
      await this.cacheManager.setIdToken(
        this.options.clientId,
        t.id_token,
        t.decodedToken
      ),
      await this.cacheManager.set(s);
  }
  async _getIdTokenFromCache() {
    const t = this.options.authorizationParams.audience || "default",
      n = await this.cacheManager.getIdToken(
        new nt({
          clientId: this.options.clientId,
          audience: t,
          scope: this.scope,
        })
      ),
      o = this.userCache.get("@@user@@");
    return n && n.id_token === (o == null ? void 0 : o.id_token)
      ? o
      : (this.userCache.set("@@user@@", n), n);
  }
  async _getEntryFromCache({ scope: t, audience: n, clientId: o }) {
    const s = await this.cacheManager.get(
      new nt({ scope: t, audience: n, clientId: o }),
      60
    );
    if (s && s.access_token) {
      const { access_token: r, oauthTokenScope: i, expires_in: c } = s,
        a = await this._getIdTokenFromCache();
      return (
        a &&
        Object.assign(
          Object.assign(
            { id_token: a.id_token, access_token: r },
            i ? { scope: i } : null
          ),
          { expires_in: c }
        )
      );
    }
  }
  async _requestToken(t, n) {
    const { nonceIn: o, organizationId: s } = n || {},
      r = await Rd(
        Object.assign(
          {
            baseUrl: this.domainUrl,
            client_id: this.options.clientId,
            auth0Client: this.options.auth0Client,
            useFormData: this.options.useFormData,
            timeout: this.httpTimeoutMs,
          },
          t
        ),
        this.worker
      ),
      i = await this._verifyIdToken(r.id_token, o, s);
    return (
      await this._saveEntryInCache(
        Object.assign(
          Object.assign(
            Object.assign(Object.assign({}, r), {
              decodedToken: i,
              scope: t.scope,
              audience: t.audience || "default",
            }),
            r.scope ? { oauthTokenScope: r.scope } : null
          ),
          { client_id: this.options.clientId }
        )
      ),
      this.cookieStorage.save(this.isAuthenticatedCookieName, !0, {
        daysUntilExpire: this.sessionCheckExpiryDays,
        cookieDomain: this.options.cookieDomain,
      }),
      this._processOrgIdHint(i.claims.org_id),
      Object.assign(Object.assign({}, r), { decodedToken: i })
    );
  }
}
function vn(e) {
  e != null &&
    e.redirect_uri &&
    (console.warn(
      "Using `redirect_uri` has been deprecated, please use `authorizationParams.redirect_uri` instead as `redirectUri` will be no longer supported in a future version"
    ),
    (e.authorizationParams = e.authorizationParams || {}),
    (e.authorizationParams.redirect_uri = e.redirect_uri),
    delete e.redirect_uri);
}
const Hd = se(null);
class Bd {
  constructor(t, n) {
    var o, s;
    (this.clientOptions = t),
      (this.pluginOptions = n),
      (this._isLoading = se(!0)),
      (this._isAuthenticated = se(!1)),
      (this._user = se({})),
      (this._idTokenClaims = se()),
      (this._error = se(null)),
      (this.isLoading = lt(this._isLoading)),
      (this.isAuthenticated = lt(this._isAuthenticated)),
      (this.user = lt(this._user)),
      (this.idTokenClaims = lt(this._idTokenClaims)),
      (this.error = lt(this._error)),
      (o = this),
      (s = ["constructor"]),
      Object.getOwnPropertyNames(Object.getPrototypeOf(o))
        .filter((r) => !s.includes(r))
        .forEach((r) => (o[r] = o[r].bind(o)));
  }
  install(t) {
    (this._client = new Kd(
      Object.assign(Object.assign({}, this.clientOptions), {
        auth0Client: { name: "auth0-vue", version: "2.2.0" },
      })
    )),
      this.__checkSession(t.config.globalProperties.$router),
      (t.config.globalProperties.$auth0 = this),
      t.provide(ha, this),
      (Hd.value = this);
  }
  async loginWithRedirect(t) {
    return vn(t), this._client.loginWithRedirect(t);
  }
  async loginWithPopup(t, n) {
    return vn(t), this.__proxy(() => this._client.loginWithPopup(t, n));
  }
  async logout(t) {
    return (t != null && t.openUrl) || (t == null ? void 0 : t.openUrl) === !1
      ? this.__proxy(() => this._client.logout(t))
      : this._client.logout(t);
  }
  async getAccessTokenSilently(t = {}) {
    return vn(t), this.__proxy(() => this._client.getTokenSilently(t));
  }
  async getAccessTokenWithPopup(t, n) {
    return vn(t), this.__proxy(() => this._client.getTokenWithPopup(t, n));
  }
  async checkSession(t) {
    return this.__proxy(() => this._client.checkSession(t));
  }
  async handleRedirectCallback(t) {
    return this.__proxy(() => this._client.handleRedirectCallback(t));
  }
  async __checkSession(t) {
    var n, o, s;
    const r = window.location.search;
    try {
      if (
        (r.includes("code=") || r.includes("error=")) &&
        r.includes("state=") &&
        !(
          !((n = this.pluginOptions) === null || n === void 0) &&
          n.skipRedirectCallback
        )
      ) {
        const i = await this.handleRedirectCallback(),
          c = i == null ? void 0 : i.appState,
          a =
            (o = c == null ? void 0 : c.target) !== null && o !== void 0
              ? o
              : "/";
        return window.history.replaceState({}, "", "/"), t && t.push(a), i;
      }
      await this.checkSession();
    } catch {
      window.history.replaceState({}, "", "/"),
        t &&
          t.push(
            ((s = this.pluginOptions) === null || s === void 0
              ? void 0
              : s.errorPath) || "/"
          );
    }
  }
  async __refreshState() {
    (this._isAuthenticated.value = await this._client.isAuthenticated()),
      (this._user.value = await this._client.getUser()),
      (this._idTokenClaims.value = await this._client.getIdTokenClaims()),
      (this._isLoading.value = !1);
  }
  async __proxy(t, n = !0) {
    let o;
    try {
      (o = await t()), (this._error.value = null);
    } catch (s) {
      throw ((this._error.value = s), s);
    } finally {
      n && (await this.__refreshState());
    }
    return o;
  }
}
function Wd(e, t) {
  return vn(e), new Bd(e, t);
}
function va() {
  return Xe(ha);
}
const En = /^[a-z0-9]+(-[a-z0-9]+)*$/,
  Ao = (e, t, n, o = "") => {
    const s = e.split(":");
    if (e.slice(0, 1) === "@") {
      if (s.length < 2 || s.length > 3) return null;
      o = s.shift().slice(1);
    }
    if (s.length > 3 || !s.length) return null;
    if (s.length > 1) {
      const c = s.pop(),
        a = s.pop(),
        l = { provider: s.length > 0 ? s[0] : o, prefix: a, name: c };
      return t && !oo(l) ? null : l;
    }
    const r = s[0],
      i = r.split("-");
    if (i.length > 1) {
      const c = { provider: o, prefix: i.shift(), name: i.join("-") };
      return t && !oo(c) ? null : c;
    }
    if (n && o === "") {
      const c = { provider: o, prefix: "", name: r };
      return t && !oo(c, n) ? null : c;
    }
    return null;
  },
  oo = (e, t) =>
    e
      ? !!(
          (e.provider === "" || e.provider.match(En)) &&
          ((t && e.prefix === "") || e.prefix.match(En)) &&
          e.name.match(En)
        )
      : !1,
  ba = Object.freeze({ left: 0, top: 0, width: 16, height: 16 }),
  mo = Object.freeze({ rotate: 0, vFlip: !1, hFlip: !1 }),
  jo = Object.freeze({ ...ba, ...mo }),
  xs = Object.freeze({ ...jo, body: "", hidden: !1 });
function Vd(e, t) {
  const n = {};
  !e.hFlip != !t.hFlip && (n.hFlip = !0),
    !e.vFlip != !t.vFlip && (n.vFlip = !0);
  const o = ((e.rotate || 0) + (t.rotate || 0)) % 4;
  return o && (n.rotate = o), n;
}
function Ii(e, t) {
  const n = Vd(e, t);
  for (const o in xs)
    o in mo
      ? o in e && !(o in n) && (n[o] = mo[o])
      : o in t
      ? (n[o] = t[o])
      : o in e && (n[o] = e[o]);
  return n;
}
function Zd(e, t) {
  const n = e.icons,
    o = e.aliases || Object.create(null),
    s = Object.create(null);
  function r(i) {
    if (n[i]) return (s[i] = []);
    if (!(i in s)) {
      s[i] = null;
      const c = o[i] && o[i].parent,
        a = c && r(c);
      a && (s[i] = [c].concat(a));
    }
    return s[i];
  }
  return (t || Object.keys(n).concat(Object.keys(o))).forEach(r), s;
}
function qd(e, t, n) {
  const o = e.icons,
    s = e.aliases || Object.create(null);
  let r = {};
  function i(c) {
    r = Ii(o[c] || s[c], r);
  }
  return i(t), n.forEach(i), Ii(e, r);
}
function wa(e, t) {
  const n = [];
  if (typeof e != "object" || typeof e.icons != "object") return n;
  e.not_found instanceof Array &&
    e.not_found.forEach((s) => {
      t(s, null), n.push(s);
    });
  const o = Zd(e);
  for (const s in o) {
    const r = o[s];
    r && (t(s, qd(e, s, r)), n.push(s));
  }
  return n;
}
const Xd = { provider: "", aliases: {}, not_found: {}, ...ba };
function Go(e, t) {
  for (const n in t) if (n in e && typeof e[n] != typeof t[n]) return !1;
  return !0;
}
function xa(e) {
  if (typeof e != "object" || e === null) return null;
  const t = e;
  if (
    typeof t.prefix != "string" ||
    !e.icons ||
    typeof e.icons != "object" ||
    !Go(e, Xd)
  )
    return null;
  const n = t.icons;
  for (const s in n) {
    const r = n[s];
    if (!s.match(En) || typeof r.body != "string" || !Go(r, xs)) return null;
  }
  const o = t.aliases || Object.create(null);
  for (const s in o) {
    const r = o[s],
      i = r.parent;
    if (!s.match(En) || typeof i != "string" || (!n[i] && !o[i]) || !Go(r, xs))
      return null;
  }
  return t;
}
const Si = Object.create(null);
function Jd(e, t) {
  return {
    provider: e,
    prefix: t,
    icons: Object.create(null),
    missing: new Set(),
  };
}
function Ht(e, t) {
  const n = Si[e] || (Si[e] = Object.create(null));
  return n[t] || (n[t] = Jd(e, t));
}
function cr(e, t) {
  return xa(t)
    ? wa(t, (n, o) => {
        o ? (e.icons[n] = o) : e.missing.add(n);
      })
    : [];
}
function Gd(e, t, n) {
  try {
    if (typeof n.body == "string") return (e.icons[t] = { ...n }), !0;
  } catch {}
  return !1;
}
let Fn = !1;
function ka(e) {
  return typeof e == "boolean" && (Fn = e), Fn;
}
function Yd(e) {
  const t = typeof e == "string" ? Ao(e, !0, Fn) : e;
  if (t) {
    const n = Ht(t.provider, t.prefix),
      o = t.name;
    return n.icons[o] || (n.missing.has(o) ? null : void 0);
  }
}
function Qd(e, t) {
  const n = Ao(e, !0, Fn);
  if (!n) return !1;
  const o = Ht(n.provider, n.prefix);
  return Gd(o, n.name, t);
}
function eh(e, t) {
  if (typeof e != "object") return !1;
  if ((typeof t != "string" && (t = e.provider || ""), Fn && !t && !e.prefix)) {
    let s = !1;
    return (
      xa(e) &&
        ((e.prefix = ""),
        wa(e, (r, i) => {
          i && Qd(r, i) && (s = !0);
        })),
      s
    );
  }
  const n = e.prefix;
  if (!oo({ provider: t, prefix: n, name: "a" })) return !1;
  const o = Ht(t, n);
  return !!cr(o, e);
}
const Ca = Object.freeze({ width: null, height: null }),
  Ia = Object.freeze({ ...Ca, ...mo }),
  th = /(-?[0-9.]*[0-9]+[0-9.]*)/g,
  nh = /^-?[0-9.]*[0-9]+[0-9.]*$/g;
function Ei(e, t, n) {
  if (t === 1) return e;
  if (((n = n || 100), typeof e == "number")) return Math.ceil(e * t * n) / n;
  if (typeof e != "string") return e;
  const o = e.split(th);
  if (o === null || !o.length) return e;
  const s = [];
  let r = o.shift(),
    i = nh.test(r);
  for (;;) {
    if (i) {
      const c = parseFloat(r);
      isNaN(c) ? s.push(r) : s.push(Math.ceil(c * t * n) / n);
    } else s.push(r);
    if (((r = o.shift()), r === void 0)) return s.join("");
    i = !i;
  }
}
const oh = (e) => e === "unset" || e === "undefined" || e === "none";
function sh(e, t) {
  const n = { ...jo, ...e },
    o = { ...Ia, ...t },
    s = { left: n.left, top: n.top, width: n.width, height: n.height };
  let r = n.body;
  [n, o].forEach((g) => {
    const y = [],
      w = g.hFlip,
      x = g.vFlip;
    let v = g.rotate;
    w
      ? x
        ? (v += 2)
        : (y.push(
            "translate(" +
              (s.width + s.left).toString() +
              " " +
              (0 - s.top).toString() +
              ")"
          ),
          y.push("scale(-1 1)"),
          (s.top = s.left = 0))
      : x &&
        (y.push(
          "translate(" +
            (0 - s.left).toString() +
            " " +
            (s.height + s.top).toString() +
            ")"
        ),
        y.push("scale(1 -1)"),
        (s.top = s.left = 0));
    let O;
    switch ((v < 0 && (v -= Math.floor(v / 4) * 4), (v = v % 4), v)) {
      case 1:
        (O = s.height / 2 + s.top),
          y.unshift("rotate(90 " + O.toString() + " " + O.toString() + ")");
        break;
      case 2:
        y.unshift(
          "rotate(180 " +
            (s.width / 2 + s.left).toString() +
            " " +
            (s.height / 2 + s.top).toString() +
            ")"
        );
        break;
      case 3:
        (O = s.width / 2 + s.left),
          y.unshift("rotate(-90 " + O.toString() + " " + O.toString() + ")");
        break;
    }
    v % 2 === 1 &&
      (s.left !== s.top && ((O = s.left), (s.left = s.top), (s.top = O)),
      s.width !== s.height &&
        ((O = s.width), (s.width = s.height), (s.height = O))),
      y.length && (r = '<g transform="' + y.join(" ") + '">' + r + "</g>");
  });
  const i = o.width,
    c = o.height,
    a = s.width,
    l = s.height;
  let u, f;
  i === null
    ? ((f = c === null ? "1em" : c === "auto" ? l : c), (u = Ei(f, a / l)))
    : ((u = i === "auto" ? a : i),
      (f = c === null ? Ei(u, l / a) : c === "auto" ? l : c));
  const d = {},
    p = (g, y) => {
      oh(y) || (d[g] = y.toString());
    };
  return (
    p("width", u),
    p("height", f),
    (d.viewBox =
      s.left.toString() +
      " " +
      s.top.toString() +
      " " +
      a.toString() +
      " " +
      l.toString()),
    { attributes: d, body: r }
  );
}
const rh = /\sid="(\S+)"/g,
  ih =
    "IconifyId" +
    Date.now().toString(16) +
    ((Math.random() * 16777216) | 0).toString(16);
let ch = 0;
function ah(e, t = ih) {
  const n = [];
  let o;
  for (; (o = rh.exec(e)); ) n.push(o[1]);
  if (!n.length) return e;
  const s = "suffix" + ((Math.random() * 16777216) | Date.now()).toString(16);
  return (
    n.forEach((r) => {
      const i = typeof t == "function" ? t(r) : t + (ch++).toString(),
        c = r.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      e = e.replace(
        new RegExp('([#;"])(' + c + ')([")]|\\.[a-z])', "g"),
        "$1" + i + s + "$3"
      );
    }),
    (e = e.replace(new RegExp(s, "g"), "")),
    e
  );
}
const ks = Object.create(null);
function lh(e, t) {
  ks[e] = t;
}
function Cs(e) {
  return ks[e] || ks[""];
}
function ar(e) {
  let t;
  if (typeof e.resources == "string") t = [e.resources];
  else if (((t = e.resources), !(t instanceof Array) || !t.length)) return null;
  return {
    resources: t,
    path: e.path || "/",
    maxURL: e.maxURL || 500,
    rotate: e.rotate || 750,
    timeout: e.timeout || 5e3,
    random: e.random === !0,
    index: e.index || 0,
    dataAfterTimeout: e.dataAfterTimeout !== !1,
  };
}
const lr = Object.create(null),
  mn = ["https://api.simplesvg.com", "https://api.unisvg.com"],
  so = [];
for (; mn.length > 0; )
  mn.length === 1 || Math.random() > 0.5
    ? so.push(mn.shift())
    : so.push(mn.pop());
lr[""] = ar({ resources: ["https://api.iconify.design"].concat(so) });
function uh(e, t) {
  const n = ar(t);
  return n === null ? !1 : ((lr[e] = n), !0);
}
function ur(e) {
  return lr[e];
}
const fh = () => {
  let e;
  try {
    if (((e = fetch), typeof e == "function")) return e;
  } catch {}
};
let Oi = fh();
function dh(e, t) {
  const n = ur(e);
  if (!n) return 0;
  let o;
  if (!n.maxURL) o = 0;
  else {
    let s = 0;
    n.resources.forEach((i) => {
      s = Math.max(s, i.length);
    });
    const r = t + ".json?icons=";
    o = n.maxURL - s - n.path.length - r.length;
  }
  return o;
}
function hh(e) {
  return e === 404;
}
const ph = (e, t, n) => {
  const o = [],
    s = dh(e, t),
    r = "icons";
  let i = { type: r, provider: e, prefix: t, icons: [] },
    c = 0;
  return (
    n.forEach((a, l) => {
      (c += a.length + 1),
        c >= s &&
          l > 0 &&
          (o.push(i),
          (i = { type: r, provider: e, prefix: t, icons: [] }),
          (c = a.length)),
        i.icons.push(a);
    }),
    o.push(i),
    o
  );
};
function mh(e) {
  if (typeof e == "string") {
    const t = ur(e);
    if (t) return t.path;
  }
  return "/";
}
const gh = (e, t, n) => {
    if (!Oi) {
      n("abort", 424);
      return;
    }
    let o = mh(t.provider);
    switch (t.type) {
      case "icons": {
        const r = t.prefix,
          c = t.icons.join(","),
          a = new URLSearchParams({ icons: c });
        o += r + ".json?" + a.toString();
        break;
      }
      case "custom": {
        const r = t.uri;
        o += r.slice(0, 1) === "/" ? r.slice(1) : r;
        break;
      }
      default:
        n("abort", 400);
        return;
    }
    let s = 503;
    Oi(e + o)
      .then((r) => {
        const i = r.status;
        if (i !== 200) {
          setTimeout(() => {
            n(hh(i) ? "abort" : "next", i);
          });
          return;
        }
        return (s = 501), r.json();
      })
      .then((r) => {
        if (typeof r != "object" || r === null) {
          setTimeout(() => {
            r === 404 ? n("abort", r) : n("next", s);
          });
          return;
        }
        setTimeout(() => {
          n("success", r);
        });
      })
      .catch(() => {
        n("next", s);
      });
  },
  _h = { prepare: ph, send: gh };
function yh(e) {
  const t = { loaded: [], missing: [], pending: [] },
    n = Object.create(null);
  e.sort((s, r) =>
    s.provider !== r.provider
      ? s.provider.localeCompare(r.provider)
      : s.prefix !== r.prefix
      ? s.prefix.localeCompare(r.prefix)
      : s.name.localeCompare(r.name)
  );
  let o = { provider: "", prefix: "", name: "" };
  return (
    e.forEach((s) => {
      if (
        o.name === s.name &&
        o.prefix === s.prefix &&
        o.provider === s.provider
      )
        return;
      o = s;
      const r = s.provider,
        i = s.prefix,
        c = s.name,
        a = n[r] || (n[r] = Object.create(null)),
        l = a[i] || (a[i] = Ht(r, i));
      let u;
      c in l.icons
        ? (u = t.loaded)
        : i === "" || l.missing.has(c)
        ? (u = t.missing)
        : (u = t.pending);
      const f = { provider: r, prefix: i, name: c };
      u.push(f);
    }),
    t
  );
}
function Sa(e, t) {
  e.forEach((n) => {
    const o = n.loaderCallbacks;
    o && (n.loaderCallbacks = o.filter((s) => s.id !== t));
  });
}
function vh(e) {
  e.pendingCallbacksFlag ||
    ((e.pendingCallbacksFlag = !0),
    setTimeout(() => {
      e.pendingCallbacksFlag = !1;
      const t = e.loaderCallbacks ? e.loaderCallbacks.slice(0) : [];
      if (!t.length) return;
      let n = !1;
      const o = e.provider,
        s = e.prefix;
      t.forEach((r) => {
        const i = r.icons,
          c = i.pending.length;
        (i.pending = i.pending.filter((a) => {
          if (a.prefix !== s) return !0;
          const l = a.name;
          if (e.icons[l]) i.loaded.push({ provider: o, prefix: s, name: l });
          else if (e.missing.has(l))
            i.missing.push({ provider: o, prefix: s, name: l });
          else return (n = !0), !0;
          return !1;
        })),
          i.pending.length !== c &&
            (n || Sa([e], r.id),
            r.callback(
              i.loaded.slice(0),
              i.missing.slice(0),
              i.pending.slice(0),
              r.abort
            ));
      });
    }));
}
let bh = 0;
function wh(e, t, n) {
  const o = bh++,
    s = Sa.bind(null, n, o);
  if (!t.pending.length) return s;
  const r = { id: o, icons: t, callback: e, abort: s };
  return (
    n.forEach((i) => {
      (i.loaderCallbacks || (i.loaderCallbacks = [])).push(r);
    }),
    s
  );
}
function xh(e, t = !0, n = !1) {
  const o = [];
  return (
    e.forEach((s) => {
      const r = typeof s == "string" ? Ao(s, t, n) : s;
      r && o.push(r);
    }),
    o
  );
}
var kh = {
  resources: [],
  index: 0,
  timeout: 2e3,
  rotate: 750,
  random: !1,
  dataAfterTimeout: !1,
};
function Ch(e, t, n, o) {
  const s = e.resources.length,
    r = e.random ? Math.floor(Math.random() * s) : e.index;
  let i;
  if (e.random) {
    let F = e.resources.slice(0);
    for (i = []; F.length > 1; ) {
      const N = Math.floor(Math.random() * F.length);
      i.push(F[N]), (F = F.slice(0, N).concat(F.slice(N + 1)));
    }
    i = i.concat(F);
  } else i = e.resources.slice(r).concat(e.resources.slice(0, r));
  const c = Date.now();
  let a = "pending",
    l = 0,
    u,
    f = null,
    d = [],
    p = [];
  typeof o == "function" && p.push(o);
  function g() {
    f && (clearTimeout(f), (f = null));
  }
  function y() {
    a === "pending" && (a = "aborted"),
      g(),
      d.forEach((F) => {
        F.status === "pending" && (F.status = "aborted");
      }),
      (d = []);
  }
  function w(F, N) {
    N && (p = []), typeof F == "function" && p.push(F);
  }
  function x() {
    return {
      startTime: c,
      payload: t,
      status: a,
      queriesSent: l,
      queriesPending: d.length,
      subscribe: w,
      abort: y,
    };
  }
  function v() {
    (a = "failed"),
      p.forEach((F) => {
        F(void 0, u);
      });
  }
  function O() {
    d.forEach((F) => {
      F.status === "pending" && (F.status = "aborted");
    }),
      (d = []);
  }
  function R(F, N, T) {
    const Z = N !== "success";
    switch (((d = d.filter((q) => q !== F)), a)) {
      case "pending":
        break;
      case "failed":
        if (Z || !e.dataAfterTimeout) return;
        break;
      default:
        return;
    }
    if (N === "abort") {
      (u = T), v();
      return;
    }
    if (Z) {
      (u = T), d.length || (i.length ? U() : v());
      return;
    }
    if ((g(), O(), !e.random)) {
      const q = e.resources.indexOf(F.resource);
      q !== -1 && q !== e.index && (e.index = q);
    }
    (a = "completed"),
      p.forEach((q) => {
        q(T);
      });
  }
  function U() {
    if (a !== "pending") return;
    g();
    const F = i.shift();
    if (F === void 0) {
      if (d.length) {
        f = setTimeout(() => {
          g(), a === "pending" && (O(), v());
        }, e.timeout);
        return;
      }
      v();
      return;
    }
    const N = {
      status: "pending",
      resource: F,
      callback: (T, Z) => {
        R(N, T, Z);
      },
    };
    d.push(N), l++, (f = setTimeout(U, e.rotate)), n(F, t, N.callback);
  }
  return setTimeout(U), x;
}
function Ea(e) {
  const t = { ...kh, ...e };
  let n = [];
  function o() {
    n = n.filter((c) => c().status === "pending");
  }
  function s(c, a, l) {
    const u = Ch(t, c, a, (f, d) => {
      o(), l && l(f, d);
    });
    return n.push(u), u;
  }
  function r(c) {
    return n.find((a) => c(a)) || null;
  }
  return {
    query: s,
    find: r,
    setIndex: (c) => {
      t.index = c;
    },
    getIndex: () => t.index,
    cleanup: o,
  };
}
function Ti() {}
const Yo = Object.create(null);
function Ih(e) {
  if (!Yo[e]) {
    const t = ur(e);
    if (!t) return;
    const n = Ea(t),
      o = { config: t, redundancy: n };
    Yo[e] = o;
  }
  return Yo[e];
}
function Sh(e, t, n) {
  let o, s;
  if (typeof e == "string") {
    const r = Cs(e);
    if (!r) return n(void 0, 424), Ti;
    s = r.send;
    const i = Ih(e);
    i && (o = i.redundancy);
  } else {
    const r = ar(e);
    if (r) {
      o = Ea(r);
      const i = e.resources ? e.resources[0] : "",
        c = Cs(i);
      c && (s = c.send);
    }
  }
  return !o || !s ? (n(void 0, 424), Ti) : o.query(t, s, n)().abort;
}
const Pi = "iconify2",
  Dn = "iconify",
  Oa = Dn + "-count",
  Ri = Dn + "-version",
  Ta = 36e5,
  Eh = 168;
function Is(e, t) {
  try {
    return e.getItem(t);
  } catch {}
}
function fr(e, t, n) {
  try {
    return e.setItem(t, n), !0;
  } catch {}
}
function Ai(e, t) {
  try {
    e.removeItem(t);
  } catch {}
}
function Ss(e, t) {
  return fr(e, Oa, t.toString());
}
function Es(e) {
  return parseInt(Is(e, Oa)) || 0;
}
const $o = { local: !0, session: !0 },
  Pa = { local: new Set(), session: new Set() };
let dr = !1;
function Oh(e) {
  dr = e;
}
let Jn = typeof window > "u" ? {} : window;
function Ra(e) {
  const t = e + "Storage";
  try {
    if (Jn && Jn[t] && typeof Jn[t].length == "number") return Jn[t];
  } catch {}
  $o[e] = !1;
}
function Aa(e, t) {
  const n = Ra(e);
  if (!n) return;
  const o = Is(n, Ri);
  if (o !== Pi) {
    if (o) {
      const c = Es(n);
      for (let a = 0; a < c; a++) Ai(n, Dn + a.toString());
    }
    fr(n, Ri, Pi), Ss(n, 0);
    return;
  }
  const s = Math.floor(Date.now() / Ta) - Eh,
    r = (c) => {
      const a = Dn + c.toString(),
        l = Is(n, a);
      if (typeof l == "string") {
        try {
          const u = JSON.parse(l);
          if (
            typeof u == "object" &&
            typeof u.cached == "number" &&
            u.cached > s &&
            typeof u.provider == "string" &&
            typeof u.data == "object" &&
            typeof u.data.prefix == "string" &&
            t(u, c)
          )
            return !0;
        } catch {}
        Ai(n, a);
      }
    };
  let i = Es(n);
  for (let c = i - 1; c >= 0; c--)
    r(c) || (c === i - 1 ? (i--, Ss(n, i)) : Pa[e].add(c));
}
function ja() {
  if (!dr) {
    Oh(!0);
    for (const e in $o)
      Aa(e, (t) => {
        const n = t.data,
          o = t.provider,
          s = n.prefix,
          r = Ht(o, s);
        if (!cr(r, n).length) return !1;
        const i = n.lastModified || -1;
        return (
          (r.lastModifiedCached = r.lastModifiedCached
            ? Math.min(r.lastModifiedCached, i)
            : i),
          !0
        );
      });
  }
}
function Th(e, t) {
  const n = e.lastModifiedCached;
  if (n && n >= t) return n === t;
  if (((e.lastModifiedCached = t), n))
    for (const o in $o)
      Aa(o, (s) => {
        const r = s.data;
        return (
          s.provider !== e.provider ||
          r.prefix !== e.prefix ||
          r.lastModified === t
        );
      });
  return !0;
}
function Ph(e, t) {
  dr || ja();
  function n(o) {
    let s;
    if (!$o[o] || !(s = Ra(o))) return;
    const r = Pa[o];
    let i;
    if (r.size) r.delete((i = Array.from(r).shift()));
    else if (((i = Es(s)), !Ss(s, i + 1))) return;
    const c = {
      cached: Math.floor(Date.now() / Ta),
      provider: e.provider,
      data: t,
    };
    return fr(s, Dn + i.toString(), JSON.stringify(c));
  }
  (t.lastModified && !Th(e, t.lastModified)) ||
    (Object.keys(t.icons).length &&
      (t.not_found && ((t = Object.assign({}, t)), delete t.not_found),
      n("local") || n("session")));
}
function ji() {}
function Rh(e) {
  e.iconsLoaderFlag ||
    ((e.iconsLoaderFlag = !0),
    setTimeout(() => {
      (e.iconsLoaderFlag = !1), vh(e);
    }));
}
function Ah(e, t) {
  e.iconsToLoad
    ? (e.iconsToLoad = e.iconsToLoad.concat(t).sort())
    : (e.iconsToLoad = t),
    e.iconsQueueFlag ||
      ((e.iconsQueueFlag = !0),
      setTimeout(() => {
        e.iconsQueueFlag = !1;
        const { provider: n, prefix: o } = e,
          s = e.iconsToLoad;
        delete e.iconsToLoad;
        let r;
        if (!s || !(r = Cs(n))) return;
        r.prepare(n, o, s).forEach((c) => {
          Sh(n, c, (a) => {
            if (typeof a != "object")
              c.icons.forEach((l) => {
                e.missing.add(l);
              });
            else
              try {
                const l = cr(e, a);
                if (!l.length) return;
                const u = e.pendingIcons;
                u &&
                  l.forEach((f) => {
                    u.delete(f);
                  }),
                  Ph(e, a);
              } catch (l) {
                console.error(l);
              }
            Rh(e);
          });
        });
      }));
}
const jh = (e, t) => {
  const n = xh(e, !0, ka()),
    o = yh(n);
  if (!o.pending.length) {
    let a = !0;
    return (
      t &&
        setTimeout(() => {
          a && t(o.loaded, o.missing, o.pending, ji);
        }),
      () => {
        a = !1;
      }
    );
  }
  const s = Object.create(null),
    r = [];
  let i, c;
  return (
    o.pending.forEach((a) => {
      const { provider: l, prefix: u } = a;
      if (u === c && l === i) return;
      (i = l), (c = u), r.push(Ht(l, u));
      const f = s[l] || (s[l] = Object.create(null));
      f[u] || (f[u] = []);
    }),
    o.pending.forEach((a) => {
      const { provider: l, prefix: u, name: f } = a,
        d = Ht(l, u),
        p = d.pendingIcons || (d.pendingIcons = new Set());
      p.has(f) || (p.add(f), s[l][u].push(f));
    }),
    r.forEach((a) => {
      const { provider: l, prefix: u } = a;
      s[l][u].length && Ah(a, s[l][u]);
    }),
    t ? wh(t, o, r) : ji
  );
};
function $h(e, t) {
  const n = { ...e };
  for (const o in t) {
    const s = t[o],
      r = typeof s;
    o in Ca
      ? (s === null || (s && (r === "string" || r === "number"))) && (n[o] = s)
      : r === typeof n[o] && (n[o] = o === "rotate" ? s % 4 : s);
  }
  return n;
}
const Lh = /[\s,]+/;
function Nh(e, t) {
  t.split(Lh).forEach((n) => {
    switch (n.trim()) {
      case "horizontal":
        e.hFlip = !0;
        break;
      case "vertical":
        e.vFlip = !0;
        break;
    }
  });
}
function Mh(e, t = 0) {
  const n = e.replace(/^-?[0-9.]*/, "");
  function o(s) {
    for (; s < 0; ) s += 4;
    return s % 4;
  }
  if (n === "") {
    const s = parseInt(e);
    return isNaN(s) ? 0 : o(s);
  } else if (n !== e) {
    let s = 0;
    switch (n) {
      case "%":
        s = 25;
        break;
      case "deg":
        s = 90;
    }
    if (s) {
      let r = parseFloat(e.slice(0, e.length - n.length));
      return isNaN(r) ? 0 : ((r = r / s), r % 1 === 0 ? o(r) : 0);
    }
  }
  return t;
}
function Fh(e, t) {
  let n =
    e.indexOf("xlink:") === -1
      ? ""
      : ' xmlns:xlink="http://www.w3.org/1999/xlink"';
  for (const o in t) n += " " + o + '="' + t[o] + '"';
  return '<svg xmlns="http://www.w3.org/2000/svg"' + n + ">" + e + "</svg>";
}
function Dh(e) {
  return e
    .replace(/"/g, "'")
    .replace(/%/g, "%25")
    .replace(/#/g, "%23")
    .replace(/</g, "%3C")
    .replace(/>/g, "%3E")
    .replace(/\s+/g, " ");
}
function Uh(e) {
  return "data:image/svg+xml," + Dh(e);
}
function zh(e) {
  return 'url("' + Uh(e) + '")';
}
const $i = { ...Ia, inline: !1 },
  Kh = {
    xmlns: "http://www.w3.org/2000/svg",
    "xmlns:xlink": "http://www.w3.org/1999/xlink",
    "aria-hidden": !0,
    role: "img",
  },
  Hh = { display: "inline-block" },
  Os = { backgroundColor: "currentColor" },
  $a = { backgroundColor: "transparent" },
  Li = { Image: "var(--svg)", Repeat: "no-repeat", Size: "100% 100%" },
  Ni = { webkitMask: Os, mask: Os, background: $a };
for (const e in Ni) {
  const t = Ni[e];
  for (const n in Li) t[e + n] = Li[n];
}
const ro = {};
["horizontal", "vertical"].forEach((e) => {
  const t = e.slice(0, 1) + "Flip";
  (ro[e + "-flip"] = t),
    (ro[e.slice(0, 1) + "-flip"] = t),
    (ro[e + "Flip"] = t);
});
function Mi(e) {
  return e + (e.match(/^[-0-9.]+$/) ? "px" : "");
}
const Fi = (e, t) => {
  const n = $h($i, t),
    o = { ...Kh },
    s = t.mode || "svg",
    r = {},
    i = t.style,
    c = typeof i == "object" && !(i instanceof Array) ? i : {};
  for (let y in t) {
    const w = t[y];
    if (w !== void 0)
      switch (y) {
        case "icon":
        case "style":
        case "onLoad":
        case "mode":
          break;
        case "inline":
        case "hFlip":
        case "vFlip":
          n[y] = w === !0 || w === "true" || w === 1;
          break;
        case "flip":
          typeof w == "string" && Nh(n, w);
          break;
        case "color":
          r.color = w;
          break;
        case "rotate":
          typeof w == "string"
            ? (n[y] = Mh(w))
            : typeof w == "number" && (n[y] = w);
          break;
        case "ariaHidden":
        case "aria-hidden":
          w !== !0 && w !== "true" && delete o["aria-hidden"];
          break;
        default: {
          const x = ro[y];
          x
            ? (w === !0 || w === "true" || w === 1) && (n[x] = !0)
            : $i[y] === void 0 && (o[y] = w);
        }
      }
  }
  const a = sh(e, n),
    l = a.attributes;
  if ((n.inline && (r.verticalAlign = "-0.125em"), s === "svg")) {
    (o.style = { ...r, ...c }), Object.assign(o, l);
    let y = 0,
      w = t.id;
    return (
      typeof w == "string" && (w = w.replace(/-/g, "_")),
      (o.innerHTML = ah(a.body, w ? () => w + "ID" + y++ : "iconifyVue")),
      Ln("svg", o)
    );
  }
  const { body: u, width: f, height: d } = e,
    p = s === "mask" || (s === "bg" ? !1 : u.indexOf("currentColor") !== -1),
    g = Fh(u, { ...l, width: f + "", height: d + "" });
  return (
    (o.style = {
      ...r,
      "--svg": zh(g),
      width: Mi(l.width),
      height: Mi(l.height),
      ...Hh,
      ...(p ? Os : $a),
      ...c,
    }),
    Ln("span", o)
  );
};
ka(!0);
lh("", _h);
if (typeof document < "u" && typeof window < "u") {
  ja();
  const e = window;
  if (e.IconifyPreload !== void 0) {
    const t = e.IconifyPreload,
      n = "Invalid IconifyPreload syntax.";
    typeof t == "object" &&
      t !== null &&
      (t instanceof Array ? t : [t]).forEach((o) => {
        try {
          (typeof o != "object" ||
            o === null ||
            o instanceof Array ||
            typeof o.icons != "object" ||
            typeof o.prefix != "string" ||
            !eh(o)) &&
            console.error(n);
        } catch {
          console.error(n);
        }
      });
  }
  if (e.IconifyProviders !== void 0) {
    const t = e.IconifyProviders;
    if (typeof t == "object" && t !== null)
      for (let n in t) {
        const o = "IconifyProviders[" + n + "] is invalid.";
        try {
          const s = t[n];
          if (typeof s != "object" || !s || s.resources === void 0) continue;
          uh(n, s) || console.error(o);
        } catch {
          console.error(o);
        }
      }
  }
}
const Bh = { ...jo, body: "" },
  Wh = $e({
    inheritAttrs: !1,
    data() {
      return { iconMounted: !1, counter: 0 };
    },
    mounted() {
      (this._name = ""), (this._loadingIcon = null), (this.iconMounted = !0);
    },
    unmounted() {
      this.abortLoading();
    },
    methods: {
      abortLoading() {
        this._loadingIcon &&
          (this._loadingIcon.abort(), (this._loadingIcon = null));
      },
      getIcon(e, t) {
        if (typeof e == "object" && e !== null && typeof e.body == "string")
          return (this._name = ""), this.abortLoading(), { data: e };
        let n;
        if (typeof e != "string" || (n = Ao(e, !1, !0)) === null)
          return this.abortLoading(), null;
        const o = Yd(n);
        if (!o)
          return (
            (!this._loadingIcon || this._loadingIcon.name !== e) &&
              (this.abortLoading(),
              (this._name = ""),
              o !== null &&
                (this._loadingIcon = {
                  name: e,
                  abort: jh([n], () => {
                    this.counter++;
                  }),
                })),
            null
          );
        this.abortLoading(), this._name !== e && ((this._name = e), t && t(e));
        const s = ["iconify"];
        return (
          n.prefix !== "" && s.push("iconify--" + n.prefix),
          n.provider !== "" && s.push("iconify--" + n.provider),
          { data: o, classes: s }
        );
      },
    },
    render() {
      this.counter;
      const e = this.$attrs,
        t = this.iconMounted ? this.getIcon(e.icon, e.onLoad) : null;
      if (!t) return Fi(Bh, e);
      let n = e;
      return (
        t.classes &&
          (n = {
            ...e,
            class:
              (typeof e.class == "string" ? e.class + " " : "") +
              t.classes.join(" "),
          }),
        Fi({ ...jo, ...t.data }, n)
      );
    },
  }),
  Vh = "modulepreload",
  Zh = function (e) {
    return "/" + e;
  },
  Di = {},
  La = function (t, n, o) {
    if (!n || n.length === 0) return t();
    const s = document.getElementsByTagName("link");
    return Promise.all(
      n.map((r) => {
        if (((r = Zh(r)), r in Di)) return;
        Di[r] = !0;
        const i = r.endsWith(".css"),
          c = i ? '[rel="stylesheet"]' : "";
        if (!!o)
          for (let u = s.length - 1; u >= 0; u--) {
            const f = s[u];
            if (f.href === r && (!i || f.rel === "stylesheet")) return;
          }
        else if (document.querySelector(`link[href="${r}"]${c}`)) return;
        const l = document.createElement("link");
        if (
          ((l.rel = i ? "stylesheet" : Vh),
          i || ((l.as = "script"), (l.crossOrigin = "")),
          (l.href = r),
          document.head.appendChild(l),
          i)
        )
          return new Promise((u, f) => {
            l.addEventListener("load", u),
              l.addEventListener("error", () =>
                f(new Error(`Unable to preload CSS for ${r}`))
              );
          });
      })
    ).then(() => t());
  },
  qh = "/logo.png",
  Xh = "/favicon.svg",
  Ot = (e, t) => {
    const n = e.__vccOpts || e;
    for (const [o, s] of t) n[o] = s;
    return n;
  },
  Jh = {},
  Gh = { class: "bl fixed m-4 z-50 row center" },
  Yh = E(
    "h1",
    { class: "row center h-16 gap-2" },
    [
      Et("Made by "),
      E("a", { href: "https://github.com/obahamonde", target: "_blank" }, [
        E("img", { src: qh, x2: "" }),
      ]),
      Et(" with "),
      E(
        "a",
        { href: "https://github.com/obahamonde/aiofauna", target: "_blank" },
        [E("img", { src: Xh, x2: "" })]
      ),
    ],
    -1
  ),
  Qh = [Yh];
function ep(e, t) {
  return V(), G("div", Gh, Qh);
}
const tp = Ot(Jh, [["render", ep]]),
  np = { class: "flex items-center justify-center" },
  op = { class: "bg-white rounded-lg shadow-lg p-8" },
  sp = { class: "modal-header" },
  rp = { class: "modal-body" },
  ip = { class: "modal-footer" },
  cp = $e({
    __name: "Modal",
    emits: ["close"],
    setup(e, { emit: t }) {
      return (n, o) => (
        V(),
        Wt(
          Ys,
          { name: "modal" },
          {
            default: rt(() => [
              E(
                "div",
                {
                  class: "fixed z-10 inset-0 overflow-y-auto",
                  onClick: o[1] || (o[1] = Gc((s) => t("close"), ["self"])),
                },
                [
                  E("div", np, [
                    E("div", op, [
                      E("div", sp, [ut(n.$slots, "header", {}, void 0, !0)]),
                      E("div", rp, [ut(n.$slots, "default", {}, void 0, !0)]),
                      E("div", ip, [
                        ut(
                          n.$slots,
                          "footer",
                          {},
                          () => [
                            E(
                              "button",
                              {
                                class: "btn-del",
                                onClick: o[0] || (o[0] = (s) => t("close")),
                              },
                              " Close "
                            ),
                          ],
                          !0
                        ),
                      ]),
                    ]),
                  ]),
                ]
              ),
            ]),
            _: 3,
          }
        )
      );
    },
  });
const hr = Ot(cp, [["__scopeId", "data-v-95b2f72a"]]),
  ht = Sd("whatsApp", () => ({
    state: st({ user: null, conversation: null, notifications: [] }),
  }));
var Ui;
const Lo = typeof window < "u",
  ap = (e) => typeof e == "string",
  lp = () => {};
Lo &&
  (Ui = window == null ? void 0 : window.navigator) != null &&
  Ui.userAgent &&
  /iP(ad|hone|od)/.test(window.navigator.userAgent);
function Ve(e) {
  return typeof e == "function" ? e() : z(e);
}
function zi(e, t = !1, n = "Timeout") {
  return new Promise((o, s) => {
    setTimeout(t ? () => s(n) : o, e);
  });
}
function up(e) {
  return e;
}
function fp(e, ...t) {
  return t.some((n) => n in e);
}
function Kn(e) {
  return Ls() ? (sc(e), !0) : !1;
}
function Qo() {
  const e = [],
    t = (s) => {
      const r = e.indexOf(s);
      r !== -1 && e.splice(r, 1);
    };
  return {
    on: (s) => {
      e.push(s);
      const r = () => t(s);
      return Kn(r), { off: r };
    },
    off: t,
    trigger: (s) => {
      e.forEach((r) => r(s));
    },
  };
}
function es(e) {
  return typeof e == "function" ? Oe(e) : se(e);
}
function Ts(e, t = !1) {
  function n(
    f,
    { flush: d = "sync", deep: p = !1, timeout: g, throwOnTimeout: y } = {}
  ) {
    let w = null;
    const v = [
      new Promise((O) => {
        w = Ee(
          e,
          (R) => {
            f(R) !== t && (w == null || w(), O(R));
          },
          { flush: d, deep: p, immediate: !0 }
        );
      }),
    ];
    return (
      g != null &&
        v.push(
          zi(g, y)
            .then(() => Ve(e))
            .finally(() => (w == null ? void 0 : w()))
        ),
      Promise.race(v)
    );
  }
  function o(f, d) {
    if (!ge(f)) return n((R) => R === f, d);
    const {
      flush: p = "sync",
      deep: g = !1,
      timeout: y,
      throwOnTimeout: w,
    } = d ?? {};
    let x = null;
    const O = [
      new Promise((R) => {
        x = Ee(
          [e, f],
          ([U, F]) => {
            t !== (U === F) && (x == null || x(), R(U));
          },
          { flush: p, deep: g, immediate: !0 }
        );
      }),
    ];
    return (
      y != null &&
        O.push(
          zi(y, w)
            .then(() => Ve(e))
            .finally(() => (x == null || x(), Ve(e)))
        ),
      Promise.race(O)
    );
  }
  function s(f) {
    return n((d) => !!d, f);
  }
  function r(f) {
    return o(null, f);
  }
  function i(f) {
    return o(void 0, f);
  }
  function c(f) {
    return n(Number.isNaN, f);
  }
  function a(f, d) {
    return n((p) => {
      const g = Array.from(p);
      return g.includes(f) || g.includes(Ve(f));
    }, d);
  }
  function l(f) {
    return u(1, f);
  }
  function u(f = 1, d) {
    let p = -1;
    return n(() => ((p += 1), p >= f), d);
  }
  return Array.isArray(Ve(e))
    ? {
        toMatch: n,
        toContains: a,
        changed: l,
        changedTimes: u,
        get not() {
          return Ts(e, !t);
        },
      }
    : {
        toMatch: n,
        toBe: o,
        toBeTruthy: s,
        toBeNull: r,
        toBeNaN: c,
        toBeUndefined: i,
        changed: l,
        changedTimes: u,
        get not() {
          return Ts(e, !t);
        },
      };
}
function dp(e) {
  return Ts(e);
}
function hp(e, t, n = {}) {
  const { immediate: o = !0 } = n,
    s = se(!1);
  let r = null;
  function i() {
    r && (clearTimeout(r), (r = null));
  }
  function c() {
    (s.value = !1), i();
  }
  function a(...l) {
    i(),
      (s.value = !0),
      (r = setTimeout(() => {
        (s.value = !1), (r = null), e(...l);
      }, Ve(t)));
  }
  return (
    o && ((s.value = !0), Lo && a()),
    Kn(c),
    { isPending: lt(s), start: a, stop: c }
  );
}
function pp(e) {
  var t;
  const n = Ve(e);
  return (t = n == null ? void 0 : n.$el) != null ? t : n;
}
const Na = Lo ? window : void 0;
function bn(...e) {
  let t, n, o, s;
  if (
    (ap(e[0]) || Array.isArray(e[0])
      ? (([n, o, s] = e), (t = Na))
      : ([t, n, o, s] = e),
    !t)
  )
    return lp;
  Array.isArray(n) || (n = [n]), Array.isArray(o) || (o = [o]);
  const r = [],
    i = () => {
      r.forEach((u) => u()), (r.length = 0);
    },
    c = (u, f, d, p) => (
      u.addEventListener(f, d, p), () => u.removeEventListener(f, d, p)
    ),
    a = Ee(
      () => [pp(t), Ve(s)],
      ([u, f]) => {
        i(), u && r.push(...n.flatMap((d) => o.map((p) => c(u, d, p, f))));
      },
      { immediate: !0, flush: "post" }
    ),
    l = () => {
      a(), i();
    };
  return Kn(l), l;
}
const Ki =
    typeof globalThis < "u"
      ? globalThis
      : typeof window < "u"
      ? window
      : typeof global < "u"
      ? global
      : typeof self < "u"
      ? self
      : {},
  Hi = "__vueuse_ssr_handlers__";
Ki[Hi] = Ki[Hi] || {};
function mp(e, t) {
  const n = se(!1);
  let o = 0;
  return (
    Lo &&
      (bn(e, "dragenter", (s) => {
        s.preventDefault(), (o += 1), (n.value = !0);
      }),
      bn(e, "dragover", (s) => {
        s.preventDefault();
      }),
      bn(e, "dragleave", (s) => {
        s.preventDefault(), (o -= 1), o === 0 && (n.value = !1);
      }),
      bn(e, "drop", (s) => {
        var r, i;
        s.preventDefault(), (o = 0), (n.value = !1);
        const c = Array.from(
          (i = (r = s.dataTransfer) == null ? void 0 : r.files) != null ? i : []
        );
        t == null || t(c.length === 0 ? null : c);
      })),
    { isOverDropZone: n }
  );
}
function gp(e, t = [], n = {}) {
  const o = se(null),
    s = se(null),
    r = se("CONNECTING"),
    i = se(null),
    c = se(null),
    { withCredentials: a = !1 } = n,
    l = () => {
      i.value && (i.value.close(), (i.value = null), (r.value = "CLOSED"));
    },
    u = new EventSource(e, { withCredentials: a });
  (i.value = u),
    (u.onopen = () => {
      (r.value = "OPEN"), (c.value = null);
    }),
    (u.onerror = (f) => {
      (r.value = "CLOSED"), (c.value = f);
    }),
    (u.onmessage = (f) => {
      (o.value = null), (s.value = f.data);
    });
  for (const f of t)
    bn(u, f, (d) => {
      (o.value = f), (s.value = d.data || null);
    });
  return (
    Kn(() => {
      l();
    }),
    { eventSource: i, event: o, data: s, status: r, error: c, close: l }
  );
}
var _p = Object.defineProperty,
  yp = Object.defineProperties,
  vp = Object.getOwnPropertyDescriptors,
  Bi = Object.getOwnPropertySymbols,
  bp = Object.prototype.hasOwnProperty,
  wp = Object.prototype.propertyIsEnumerable,
  Wi = (e, t, n) =>
    t in e
      ? _p(e, t, { enumerable: !0, configurable: !0, writable: !0, value: n })
      : (e[t] = n),
  Le = (e, t) => {
    for (var n in t || (t = {})) bp.call(t, n) && Wi(e, n, t[n]);
    if (Bi) for (var n of Bi(t)) wp.call(t, n) && Wi(e, n, t[n]);
    return e;
  },
  gn = (e, t) => yp(e, vp(t));
const xp = { json: "application/json", text: "text/plain" };
function Vi(e) {
  return (
    e &&
    fp(
      e,
      "immediate",
      "refetch",
      "initialData",
      "timeout",
      "beforeFetch",
      "afterFetch",
      "onFetchError",
      "fetch"
    )
  );
}
function ts(e) {
  return typeof Headers < "u" && e instanceof Headers
    ? Object.fromEntries([...e.entries()])
    : e;
}
function On(e, ...t) {
  var n;
  const o = typeof AbortController == "function";
  let s = {},
    r = { immediate: !0, refetch: !1, timeout: 0 };
  const i = { method: "GET", type: "text", payload: void 0 };
  t.length > 0 && (Vi(t[0]) ? (r = Le(Le({}, r), t[0])) : (s = t[0])),
    t.length > 1 && Vi(t[1]) && (r = Le(Le({}, r), t[1]));
  const {
      fetch: c = (n = Na) == null ? void 0 : n.fetch,
      initialData: a,
      timeout: l,
    } = r,
    u = Qo(),
    f = Qo(),
    d = Qo(),
    p = se(!1),
    g = se(!1),
    y = se(!1),
    w = se(null),
    x = Qn(null),
    v = Qn(null),
    O = Qn(a),
    R = Oe(() => o && g.value);
  let U, F;
  const N = () => {
      o && U && (U.abort(), (U = void 0));
    },
    T = (ee) => {
      (g.value = ee), (p.value = !ee);
    };
  l && (F = hp(N, l, { immediate: !1 }));
  const Z = async (ee = !1) => {
      var ce;
      T(!0),
        (v.value = null),
        (w.value = null),
        (y.value = !1),
        o &&
          (N(),
          (U = new AbortController()),
          (U.signal.onabort = () => (y.value = !0)),
          (s = gn(Le({}, s), { signal: U.signal })));
      const Q = { method: i.method, headers: {} };
      if (i.payload) {
        const Ae = ts(Q.headers);
        i.payloadType &&
          (Ae["Content-Type"] =
            (ce = xp[i.payloadType]) != null ? ce : i.payloadType);
        const ke = Ve(i.payload);
        Q.body = i.payloadType === "json" ? JSON.stringify(ke) : ke;
      }
      let te = !1;
      const xe = {
        url: Ve(e),
        options: Le(Le({}, Q), s),
        cancel: () => {
          te = !0;
        },
      };
      if (
        (r.beforeFetch && Object.assign(xe, await r.beforeFetch(xe)), te || !c)
      )
        return T(!1), Promise.resolve(null);
      let Ie = null;
      return (
        F && F.start(),
        new Promise((Ae, ke) => {
          var it;
          c(
            xe.url,
            gn(Le(Le({}, Q), xe.options), {
              headers: Le(
                Le({}, ts(Q.headers)),
                ts((it = xe.options) == null ? void 0 : it.headers)
              ),
            })
          )
            .then(async (ye) => {
              if (
                ((x.value = ye),
                (w.value = ye.status),
                (Ie = await ye[i.type]()),
                r.afterFetch &&
                  w.value >= 200 &&
                  w.value < 300 &&
                  ({ data: Ie } = await r.afterFetch({
                    data: Ie,
                    response: ye,
                  })),
                (O.value = Ie),
                !ye.ok)
              )
                throw new Error(ye.statusText);
              return u.trigger(ye), Ae(ye);
            })
            .catch(async (ye) => {
              let Tt = ye.message || ye.name;
              return (
                r.onFetchError &&
                  ({ data: Ie, error: Tt } = await r.onFetchError({
                    data: Ie,
                    error: ye,
                    response: x.value,
                  })),
                (O.value = Ie),
                (v.value = Tt),
                f.trigger(ye),
                ee ? ke(ye) : Ae(null)
              );
            })
            .finally(() => {
              T(!1), F && F.stop(), d.trigger(null);
            });
        })
      );
    },
    q = es(r.refetch);
  Ee([q, es(e)], ([ee]) => ee && Z(), { deep: !0 });
  const ae = {
    isFinished: p,
    statusCode: w,
    response: x,
    error: v,
    data: O,
    isFetching: g,
    canAbort: R,
    aborted: y,
    abort: N,
    execute: Z,
    onFetchResponse: u.on,
    onFetchError: f.on,
    onFetchFinally: d.on,
    get: L("GET"),
    put: L("PUT"),
    post: L("POST"),
    delete: L("DELETE"),
    patch: L("PATCH"),
    head: L("HEAD"),
    options: L("OPTIONS"),
    json: de("json"),
    text: de("text"),
    blob: de("blob"),
    arrayBuffer: de("arrayBuffer"),
    formData: de("formData"),
  };
  function L(ee) {
    return (ce, Q) => {
      if (!g.value) {
        (i.method = ee),
          (i.payload = ce),
          (i.payloadType = Q),
          ge(i.payload) &&
            Ee([q, es(i.payload)], ([xe]) => xe && Z(), { deep: !0 });
        const te = Ve(i.payload);
        return (
          !Q &&
            te &&
            Object.getPrototypeOf(te) === Object.prototype &&
            !(te instanceof FormData) &&
            (i.payloadType = "json"),
          gn(Le({}, ae), {
            then(xe, Ie) {
              return oe().then(xe, Ie);
            },
          })
        );
      }
    };
  }
  function oe() {
    return new Promise((ee, ce) => {
      dp(p)
        .toBe(!0)
        .then(() => ee(ae))
        .catch((Q) => ce(Q));
    });
  }
  function de(ee) {
    return () => {
      if (!g.value)
        return (
          (i.type = ee),
          gn(Le({}, ae), {
            then(ce, Q) {
              return oe().then(ce, Q);
            },
          })
        );
    };
  }
  return (
    r.immediate && setTimeout(Z, 0),
    gn(Le({}, ae), {
      then(ee, ce) {
        return oe().then(ee, ce);
      },
    })
  );
}
function kp(e) {
  const t = se(),
    n = () => {
      t.value && URL.revokeObjectURL(t.value), (t.value = void 0);
    };
  return (
    Ee(
      () => z(e),
      (o) => {
        n(), o && (t.value = URL.createObjectURL(o));
      },
      { immediate: !0 }
    ),
    Kn(n),
    lt(t)
  );
}
var Zi;
(function (e) {
  (e.UP = "UP"),
    (e.RIGHT = "RIGHT"),
    (e.DOWN = "DOWN"),
    (e.LEFT = "LEFT"),
    (e.NONE = "NONE");
})(Zi || (Zi = {}));
var Cp = Object.defineProperty,
  qi = Object.getOwnPropertySymbols,
  Ip = Object.prototype.hasOwnProperty,
  Sp = Object.prototype.propertyIsEnumerable,
  Xi = (e, t, n) =>
    t in e
      ? Cp(e, t, { enumerable: !0, configurable: !0, writable: !0, value: n })
      : (e[t] = n),
  Ep = (e, t) => {
    for (var n in t || (t = {})) Ip.call(t, n) && Xi(e, n, t[n]);
    if (qi) for (var n of qi(t)) Sp.call(t, n) && Xi(e, n, t[n]);
    return e;
  };
const Op = {
  easeInSine: [0.12, 0, 0.39, 0],
  easeOutSine: [0.61, 1, 0.88, 1],
  easeInOutSine: [0.37, 0, 0.63, 1],
  easeInQuad: [0.11, 0, 0.5, 0],
  easeOutQuad: [0.5, 1, 0.89, 1],
  easeInOutQuad: [0.45, 0, 0.55, 1],
  easeInCubic: [0.32, 0, 0.67, 0],
  easeOutCubic: [0.33, 1, 0.68, 1],
  easeInOutCubic: [0.65, 0, 0.35, 1],
  easeInQuart: [0.5, 0, 0.75, 0],
  easeOutQuart: [0.25, 1, 0.5, 1],
  easeInOutQuart: [0.76, 0, 0.24, 1],
  easeInQuint: [0.64, 0, 0.78, 0],
  easeOutQuint: [0.22, 1, 0.36, 1],
  easeInOutQuint: [0.83, 0, 0.17, 1],
  easeInExpo: [0.7, 0, 0.84, 0],
  easeOutExpo: [0.16, 1, 0.3, 1],
  easeInOutExpo: [0.87, 0, 0.13, 1],
  easeInCirc: [0.55, 0, 1, 0.45],
  easeOutCirc: [0, 0.55, 0.45, 1],
  easeInOutCirc: [0.85, 0, 0.15, 1],
  easeInBack: [0.36, 0, 0.66, -0.56],
  easeOutBack: [0.34, 1.56, 0.64, 1],
  easeInOutBack: [0.68, -0.6, 0.32, 1.6],
};
Ep({ linear: up }, Op);
const Tp = { class: "flex gap-4 max-h-400px" },
  Pp = { class: "w-full relative rounded-lg sh" },
  Rp = { class: "col center m-8" },
  Ap = { key: 0, class: "grid3 p-8 gap-8" },
  jp = { class: "row gap-4" },
  $p = { class: "text-sm text-body" },
  Lp = { class: "text-sm text-body" },
  Np = { class: "text-sm text-body" },
  Mp = { class: "text-sm text-body" },
  Fp = { class: "col center p-8" },
  Dp = { key: 0 },
  Up = ["href"],
  zp = ["src"],
  Kp = { key: 1 },
  Hp = ["src"],
  Bp = ["href"],
  Wp = { key: 2 },
  Vp = ["href"],
  Zp = ["src"],
  qp = { key: 3 },
  Xp = ["href"],
  Jp = $e({
    __name: "MessageUpload",
    setup(e) {
      const t = st([]),
        n = st([]),
        { state: o } = ht(),
        s = async (u) => {
          !u ||
            u.length === 0 ||
            (u
              .map((f) => {
                const d = kp(f);
                return {
                  user: o.user.ref,
                  name: f.name,
                  key: o.user.ref,
                  url: d.value,
                  type: f.type,
                  lastModified: f.lastModified,
                  file: f,
                };
              })
              .forEach(async (f) => {
                t.push(f);
                const d = new FormData();
                d.append("file", f.file);
                const { data: p } = await On(
                  `/api/upload?key=${f.key}&size=${f.file.size}&user=${f.user}`,
                  { method: "POST", body: d }
                ).json();
                n.push(z(p));
              }),
            await l());
        },
        r = se(),
        { isOverDropZone: i } = mp(r, s),
        c = () => {
          const u = document.createElement("input");
          (u.onchange = (f) => {
            const d = f.target.files;
            s(Array.from(d));
          }),
            u.setAttribute("type", "file"),
            u.setAttribute("multiple", "true"),
            u.setAttribute("accept", "*/*"),
            u.click();
        },
        a = async (u) => {
          await On(`/api/upload?ref=${u.ref}`, { method: "DELETE" }).json(),
            t.splice(t.indexOf(u), 1),
            n.splice(n.indexOf(u), 1),
            await l(),
            o.notifications.push({
              status: "success",
              message: "File deleted",
            });
        },
        l = async () => {
          const { data: u } = await On(`/api/upload?user=${o.user.ref}`, {
            method: "GET",
          }).json();
          z(u).forEach((d) => {
            n.push(d);
          });
        };
      return (
        Un(async () => {
          await l();
        }),
        (u, f) => {
          const d = It("Icon");
          return (
            V(),
            G("div", Tp, [
              E("div", Pp, [
                E(
                  "div",
                  {
                    ref_key: "dropZoneRef",
                    ref: r,
                    onClick: c,
                    multiple: "",
                    class:
                      "flex flex-col w-full min-h-200px h-auto bg-gray-400/10 justify-center items-center mt-6",
                  },
                  [
                    E(
                      "div",
                      null,
                      Ce(z(i) ? "Drop here" : "Drag and drop files here"),
                      1
                    ),
                  ],
                  512
                ),
                E("div", Rp, [
                  z(t).length > 0
                    ? (V(),
                      G("div", Ap, [
                        (V(!0),
                        G(
                          _e,
                          null,
                          zn(
                            z(n),
                            (p, g) => (
                              V(),
                              G(
                                "div",
                                {
                                  key: g,
                                  class: "col bg-gray-100 sh center gap-2 p-4",
                                },
                                [
                                  E("p", jp, [
                                    J(
                                      d,
                                      {
                                        icon: "mdi-close",
                                        onClick: (y) => a(p),
                                        class:
                                          "x2 cp hover:red-700 text-red-500 scale",
                                      },
                                      null,
                                      8,
                                      ["onClick"]
                                    ),
                                  ]),
                                  E("p", $p, Ce(p.name), 1),
                                  E(
                                    "p",
                                    Lp,
                                    Ce((p.size / 1e3).toFixed(2)) + " Kb ",
                                    1
                                  ),
                                  E("p", Np, Ce(p.type), 1),
                                  E(
                                    "p",
                                    Mp,
                                    Ce(
                                      new Date(p.lastModified).toLocaleString()
                                    ),
                                    1
                                  ),
                                  E("div", Fp, [
                                    p.type.includes("image")
                                      ? (V(),
                                        G("div", Dp, [
                                          E(
                                            "a",
                                            { href: p.url, target: "_blank" },
                                            [
                                              E(
                                                "img",
                                                { src: p.url },
                                                null,
                                                8,
                                                zp
                                              ),
                                            ],
                                            8,
                                            Up
                                          ),
                                        ]))
                                      : p.type.includes("video")
                                      ? (V(),
                                        G("div", Kp, [
                                          E(
                                            "video",
                                            { controls: "", src: p.url },
                                            null,
                                            8,
                                            Hp
                                          ),
                                          E(
                                            "a",
                                            { href: p.url, target: "_blank" },
                                            [
                                              J(d, {
                                                icon: "mdi-video",
                                                class: "x4",
                                              }),
                                            ],
                                            8,
                                            Bp
                                          ),
                                        ]))
                                      : p.type.includes("audio")
                                      ? (V(),
                                        G("div", Wp, [
                                          E(
                                            "a",
                                            { href: p.url, target: "_blank" },
                                            [
                                              J(d, {
                                                icon: "mdi-music",
                                                class: "x4",
                                              }),
                                            ],
                                            8,
                                            Vp
                                          ),
                                          E(
                                            "audio",
                                            { controls: "", src: p.url },
                                            null,
                                            8,
                                            Zp
                                          ),
                                        ]))
                                      : (V(),
                                        G("div", qp, [
                                          E(
                                            "a",
                                            { href: p.url, target: "_blank" },
                                            [
                                              J(d, {
                                                icon: "mdi-file",
                                                class: "x4",
                                              }),
                                            ],
                                            8,
                                            Xp
                                          ),
                                        ])),
                                  ]),
                                ]
                              )
                            )
                          ),
                          128
                        )),
                      ]))
                    : un("", !0),
                ]),
              ]),
            ])
          );
        }
      );
    },
  }),
  pr = () => {
    const e = se(null),
      t = se(null),
      n = se(!1);
    return {
      response: e,
      iserror: t,
      isloading: n,
      request: async (s, r) => {
        const {
          data: i,
          error: c,
          isFetching: a,
        } = await On(s, r, { refetch: !0 }).json();
        (e.value = z(i)), (t.value = z(c)), (n.value = z(a.value));
        const l = async () => {
          const {
            data: u,
            error: f,
            isFetching: d,
          } = await On(s, r, { refetch: !0 }).json();
          (e.value = z(u)), (t.value = z(f)), (n.value = z(d.value));
        };
        Un(() => {
          l();
        }),
          Ee(e, () => {
            l();
          });
      },
    };
  },
  Gp = { class: "chatbox-input" },
  Yp = E("i", { class: "fa-regular fa-face-grin" }, null, -1),
  Qp = E("i", { class: "fa-solid fa-microphone" }, null, -1),
  em = $e({
    __name: "MessageInput",
    setup(e) {
      const { request: t, response: n } = pr(),
        { state: o } = ht(),
        s = async () => {
          !o.conversation.ref ||
            !o.user.ref ||
            !r.value ||
            (await t("/api/messages", {
              method: "POST",
              body: JSON.stringify({
                text: r.value,
                user: o.user.ref,
                conversation: o.conversation.ref,
                kind: "TEXT",
              }),
            }),
            (r.value = ""));
        };
      Ee(
        () => n.value,
        (c) => {
          c && (o.conversation = c);
        }
      );
      const r = se(""),
        i = se(!1);
      return (c, a) => {
        const l = Jp,
          u = hr;
        return (
          V(),
          G(
            _e,
            null,
            [
              E("div", Gp, [
                Yp,
                E("i", {
                  class: "fa-sharp fa-solid fa-paperclip",
                  onClick: a[0] || (a[0] = (f) => (i.value = !i.value)),
                }),
                Oc(
                  E(
                    "input",
                    {
                      type: "text",
                      placeholder: "Type a message",
                      "onUpdate:modelValue":
                        a[1] || (a[1] = (f) => (r.value = f)),
                      onKeyup: a[2] || (a[2] = df((f) => s(), ["enter"])),
                    },
                    null,
                    544
                  ),
                  [[Jc, r.value]]
                ),
                Qp,
              ]),
              i.value
                ? (V(),
                  Wt(
                    u,
                    { key: 0, onClose: a[3] || (a[3] = (f) => (i.value = !1)) },
                    { default: rt(() => [J(l)]), _: 1 }
                  ))
                : un("", !0),
            ],
            64
          )
        );
      };
    },
  }),
  tm = (e) => {
    const {
        status: t,
        data: n,
        eventSource: o,
        close: s,
      } = gp(`${e.url}?ref=${e.query}`),
      r = se([]);
    return (
      Ee(n, (i) => {
        i && r.value.push(JSON.parse(i));
      }),
      Zs(() => {
        s();
      }),
      { messages: r, status: t, eventSource: o }
    );
  },
  nm = { key: 0 },
  om = { key: 1 },
  sm = { key: 2 },
  rm = E("p", { class: "text-error" }, "Connection closed", -1),
  im = $e({
    __name: "Sse",
    props: {
      url: { type: String, required: !1, default: "/api/sse" },
      query: { type: String, required: !0 },
    },
    setup(e) {
      const t = e,
        { messages: n, eventSource: o, status: s } = tm(t),
        r = Oe(() => s.value);
      return (
        Ee(o, (i, c) => {
          c && c.close(), (o.value = i);
        }),
        (i, c) => {
          const a = It("Icon");
          return z(r) === "OPEN"
            ? (V(),
              G("div", nm, [
                (V(!0),
                G(
                  _e,
                  null,
                  zn(
                    z(n),
                    (l) => (
                      V(), G("div", null, [ut(i.$slots, "default", { sse: l })])
                    )
                  ),
                  256
                )),
              ]))
            : z(r) === "CONNECTING"
            ? (V(),
              G("div", om, [
                ut(i.$slots, "loading", {}, () => [
                  J(a, { icon: "mdi-loading", "animate-spin": "", x2: "" }),
                ]),
              ]))
            : z(r) === "CLOSED"
            ? (V(), G("div", sm, [ut(i.$slots, "error", {}, () => [rm])]))
            : un("", !0);
        }
      );
    },
  }),
  cm = { key: 0 },
  am = { key: 1 },
  lm = { class: "text-error" },
  um = { key: 2 },
  mr = $e({
    __name: "Request",
    props: {
      url: { type: String, required: !0 },
      options: {
        type: Object,
        required: !1,
        default: () => ({
          method: "GET",
          headers: { "Content-Type": "application/json" },
        }),
      },
    },
    setup(e) {
      const t = e,
        { request: n, response: o, iserror: s, isloading: r } = pr(),
        { state: i } = ht(),
        c = async () => {
          await n(t.url, t.options);
        };
      Un(c);
      const a = st(t);
      Ee(a, c),
        Sc(() => {
          s.value &&
            i.notifications.push({
              status: "error",
              message:
                typeof s.value == "string" ? s.value : JSON.stringify(s.value),
            });
        });
      const l = Oe(() => r.value);
      return (u, f) => {
        const d = It("Icon");
        return !z(s) && !z(l) && z(o)
          ? (V(), G("div", cm, [ut(u.$slots, "default", { json: z(o) })]))
          : z(s)
          ? (V(),
            G("div", am, [
              ut(u.$slots, "error", { error: z(s) }, () => [
                E("p", lm, "An error occurred: " + Ce(z(s).message), 1),
              ]),
            ]))
          : z(l)
          ? (V(),
            G("div", um, [
              ut(u.$slots, "loading", {}, () => [
                J(d, { icon: "mdi-loading", "animate-spin": "", x2: "" }),
              ]),
            ]))
          : un("", !0);
      };
    },
  }),
  fm = { class: "chat-container" },
  dm = { key: 0 },
  hm = E("br", null, null, -1),
  pm = E("br", null, null, -1),
  mm = { key: 1, class: "chat-container" },
  gm = E(
    "h1",
    { class: "text-center px-4 py-2 rounded-lg bg-gray-300 w-64 mx-auto" },
    "Select a conversation to start chatting ",
    -1
  ),
  _m = [gm],
  ym = $e({
    __name: "ChatContainer",
    setup(e) {
      const { state: t } = ht();
      return (n, o) => {
        const s = mr,
          r = im;
        return (
          V(),
          G("div", fm, [
            z(t).conversation
              ? (V(),
                G("div", dm, [
                  J(
                    s,
                    { url: "/api/messages/" + z(t).conversation.ref },
                    {
                      default: rt((i) => [
                        (V(!0),
                        G(
                          _e,
                          null,
                          zn(
                            i.json,
                            (c) => (
                              V(),
                              G("div", null, [
                                E(
                                  "div",
                                  {
                                    class: Kt(
                                      z(t).user.ref === c.owner
                                        ? "message-box my-message"
                                        : "message-box friend-message"
                                    ),
                                  },
                                  [
                                    E("p", null, [
                                      Et(Ce(c.text), 1),
                                      hm,
                                      E(
                                        "span",
                                        null,
                                        Ce(
                                          new Date(
                                            Number(c.ts)
                                          ).toLocaleString()
                                        ),
                                        1
                                      ),
                                    ]),
                                  ],
                                  2
                                ),
                              ])
                            )
                          ),
                          256
                        )),
                      ]),
                      _: 1,
                    },
                    8,
                    ["url"]
                  ),
                  J(
                    r,
                    { query: z(t).conversation.ref },
                    {
                      default: rt((i) => [
                        E("div", null, [
                          E(
                            "div",
                            {
                              class: Kt(
                                z(t).user.ref === i.sse.user
                                  ? "message-box my-message"
                                  : "message-box friend-message"
                              ),
                            },
                            [
                              E("p", null, [
                                Et(Ce(i.sse.text), 1),
                                pm,
                                E(
                                  "span",
                                  null,
                                  Ce(
                                    new Date(Number(i.sse.ts)).toLocaleString()
                                  ),
                                  1
                                ),
                              ]),
                            ],
                            2
                          ),
                        ]),
                      ]),
                      _: 1,
                    },
                    8,
                    ["query"]
                  ),
                ]))
              : (V(), G("div", mm, _m)),
          ])
        );
      };
    },
  }),
  vm = { key: 0, class: "header py-2" },
  bm = { class: "img-text" },
  wm = { class: "user-img" },
  xm = ["src"],
  km = E("br", null, null, -1),
  Cm = { key: 0, class: "online" },
  Im = { key: 1, class: "offline" },
  Sm = E(
    "div",
    { class: "nav-icons" },
    [
      E("li", null, [E("i", { class: "fa-solid fa-magnifying-glass" })]),
      E("li", null, [E("i", { class: "fa-solid fa-ellipsis-vertical" })]),
    ],
    -1
  ),
  Em = { key: 1, class: "header" },
  Om = { class: "chat-slug" },
  Tm = $e({
    __name: "ChatHeader",
    setup(e) {
      const { state: t } = ht(),
        n = (s) => navigator.clipboard.writeText(s),
        o = se(!1);
      return (s, r) => {
        const i = It("Icon"),
          c = mr;
        return z(t).conversation
          ? (V(),
            G("div", vm, [
              E("div", bm, [
                E("div", wm, [
                  E(
                    "img",
                    {
                      class: "dp",
                      src: z(t).conversation.guest.picture,
                      alt: "",
                    },
                    null,
                    8,
                    xm
                  ),
                ]),
                E("h4", null, [
                  Et(Ce(z(t).conversation.guest.name), 1),
                  km,
                  J(
                    c,
                    { url: "/api/online/" + z(t).conversation.guest.ref },
                    {
                      default: rt((a) => [
                        E(
                          "small",
                          {
                            class: Kt([
                              "text-xs gap-4 row",
                              z(o) ? "" : "opacity-0 fixed",
                            ]),
                            onMouseover: r[1] || (r[1] = (l) => (o.value = !0)),
                            onMouseleave:
                              r[2] || (r[2] = (l) => (o.value = !1)),
                          },
                          [
                            Et(Ce(z(t).conversation.guest.ref) + " ", 1),
                            J(i, {
                              icon: "mdi-clipboard",
                              onClick:
                                r[0] ||
                                (r[0] = (l) => n(z(t).conversation.guest.ref)),
                            }),
                          ],
                          34
                        ),
                        a.json.online
                          ? (V(), G("span", Cm, "Online"))
                          : (V(),
                            G(
                              "span",
                              Im,
                              "Last Seen: " +
                                Ce(
                                  new Date(
                                    Number(z(t).conversation.ts)
                                  ).toLocaleTimeString()
                                ),
                              1
                            )),
                      ]),
                      _: 1,
                    },
                    8,
                    ["url"]
                  ),
                ]),
              ]),
              Sm,
            ]))
          : (V(),
            G("div", Em, [E("div", Om, Ce(new Date().toLocaleString()), 1)]));
      };
    },
  }),
  Pm = {},
  Rm = { class: "right-container" };
function Am(e, t) {
  const n = Tm,
    o = ym,
    s = em;
  return V(), G("div", Rm, [J(n), J(o), J(s)]);
}
const jm = Ot(Pm, [["render", Am]]),
  $m = { class: "chat-list" },
  Lm = ["onClick"],
  Nm = { class: "img-box" },
  Mm = ["src", "alt"],
  Fm = { class: "chat-details" },
  Dm = { class: "text-head" },
  Um = { class: "time unread text-xs row" },
  zm = { class: "text-message" },
  Km = $e({
    __name: "ChatList",
    setup(e) {
      const { state: t } = ht(),
        n = se(null),
        o = async (s) => {
          n.value = s;
        };
      return (
        Ee(n, (s) => {
          t.conversation = s;
        }),
        (s, r) => {
          const i = mr;
          return (
            V(),
            Wt(
              i,
              { url: "/api/conversations/" + z(t).user.ref },
              {
                default: rt((c) => [
                  E("div", $m, [
                    (V(!0),
                    G(
                      _e,
                      null,
                      zn(
                        c.json,
                        (a) => (
                          V(),
                          G(
                            "div",
                            { class: "chat-box", onClick: (l) => o(a) },
                            [
                              E("div", Nm, [
                                E(
                                  "img",
                                  {
                                    class: "img-cover",
                                    src: a.guest.picture,
                                    alt: a.guest.ref,
                                  },
                                  null,
                                  8,
                                  Mm
                                ),
                              ]),
                              E("div", Fm, [
                                E("div", Dm, [
                                  E(
                                    "h4",
                                    null,
                                    Ce(a.guest.name.split(" ")[0]),
                                    1
                                  ),
                                  E(
                                    "span",
                                    Um,
                                    Ce(
                                      new Date(
                                        Number(a.ts)
                                      ).toLocaleTimeString()
                                    ),
                                    1
                                  ),
                                ]),
                                E("div", zm, [
                                  E(
                                    "p",
                                    null,
                                    Ce(
                                      a.messages.length > 0
                                        ? a.messages.reverse()[0].text
                                        : "[Start the conversation]"
                                    ),
                                    1
                                  ),
                                  E(
                                    "b",
                                    null,
                                    Ce(
                                      a.messages.reduce(
                                        (l, u) => (u.read ? l : l + 1),
                                        0
                                      )
                                    ),
                                    1
                                  ),
                                ]),
                              ]),
                            ],
                            8,
                            Lm
                          )
                        )
                      ),
                      256
                    )),
                  ]),
                ]),
                _: 1,
              },
              8,
              ["url"]
            )
          );
        }
      );
    },
  }),
  Hm = { class: "search-container" },
  Bm = { class: "input" },
  Wm = E(
    "input",
    { type: "text", placeholder: "Search or start new chat" },
    null,
    -1
  ),
  Vm = E("i", { class: "fa-sharp fa-solid fa-bars-filter" }, null, -1),
  Zm = $e({
    __name: "SearchContact",
    setup(e) {
      const t = se(!1);
      return (n, o) => {
        const s = hr;
        return (
          V(),
          G("div", Hm, [
            E("div", Bm, [
              E("i", {
                class: "fa-solid fa-magnifying-glass",
                onClick: o[0] || (o[0] = (r) => (t.value = !z(t))),
              }),
              Wm,
            ]),
            Vm,
            z(t)
              ? (V(),
                Wt(s, {
                  key: 0,
                  onClose: o[1] || (o[1] = (r) => (t.value = !1)),
                }))
              : un("", !0),
          ])
        );
      };
    },
  }),
  qm = { class: "header" },
  Xm = { class: "user-img" },
  Jm = ["src", "alt"],
  Gm = { class: "nav-icons" },
  Ym = E("li", null, [E("i", { class: "fa-solid fa-users" })], -1),
  Qm = E("li", null, [E("i", { class: "fa-solid fa-ellipsis-vertical" })], -1),
  eg = { class: "col center" },
  tg = E("label", { for: "number" }, "Number:", -1),
  ng = E("br", null, null, -1),
  og = E("br", null, null, -1),
  sg = $e({
    __name: "UserHeader",
    setup(e) {
      const { state: t } = ht(),
        { logout: n } = va(),
        o = se(!1),
        s = se(""),
        { request: r, response: i } = pr(),
        c = async () => {
          const a = t.user.ref;
          !s.value ||
            !a ||
            (await r("/api/new_conversation/" + a + "?contact=" + s.value, {
              method: "GET",
              headers: { "Content-Type": "application/json" },
            }),
            (t.conversation = i));
        };
      return (a, l) => {
        const u = hr;
        return (
          V(),
          G(
            _e,
            null,
            [
              E("div", qm, [
                E("div", Xm, [
                  E(
                    "img",
                    {
                      class: "dp",
                      src: z(t).user.picture,
                      alt: z(t).user.name,
                      onClick: l[0] || (l[0] = (f) => z(n)()),
                    },
                    null,
                    8,
                    Jm
                  ),
                ]),
                E("div", Gm, [
                  Ym,
                  E("li", null, [
                    E("i", {
                      class: "fa-solid fa-message",
                      onClick: l[1] || (l[1] = (f) => (o.value = !z(o))),
                    }),
                  ]),
                  Qm,
                ]),
              ]),
              z(o)
                ? (V(),
                  Wt(
                    u,
                    { key: 0, onClose: l[4] || (l[4] = (f) => (o.value = !1)) },
                    {
                      default: rt(() => [
                        E("template", eg, [
                          tg,
                          Oc(
                            E(
                              "input",
                              {
                                type: "text",
                                id: "number",
                                name: "number",
                                "input-text": "",
                                "onUpdate:modelValue":
                                  l[2] ||
                                  (l[2] = (f) =>
                                    ge(s) ? (s.value = f) : null),
                              },
                              null,
                              512
                            ),
                            [[Jc, z(s)]]
                          ),
                          ng,
                          og,
                        ]),
                        E(
                          "button",
                          {
                            onClick: l[3] || (l[3] = (f) => c()),
                            "btn-get": "",
                          },
                          "Add Contact"
                        ),
                      ]),
                      _: 1,
                    }
                  ))
                : un("", !0),
            ],
            64
          )
        );
      };
    },
  }),
  rg = {},
  ig = { class: "left-container" };
function cg(e, t) {
  const n = sg,
    o = Zm,
    s = Km;
  return V(), G("div", ig, [J(n), J(o), J(s)]);
}
const ag = Ot(rg, [["render", cg]]),
  lg = {},
  ug = { row: "", tr: "", fixed: "", "gap-4": "", "mt-8": "" };
function fg(e, t) {
  const n = It("Icon"),
    o = It("RouterLink");
  return (
    V(),
    G("nav", ug, [
      J(
        o,
        { to: "/" },
        {
          default: rt(() => [
            J(n, {
              icon: "logos:whatsapp-icon",
              x4: "",
              "mx-4": "",
              "icon-btn": "",
            }),
          ]),
          _: 1,
        }
      ),
      J(
        o,
        { to: "/test" },
        {
          default: rt(() => [
            J(n, {
              icon: "logos:testlodge",
              x4: "",
              "mx-4": "",
              "icon-btn": "",
            }),
          ]),
          _: 1,
        }
      ),
    ])
  );
}
const Ma = Ot(lg, [["render", fg]]),
  dg = {};
function hg(e, t) {
  const n = Ma,
    o = ag,
    s = jm;
  return V(), G(_e, null, [J(n), J(o), J(s)], 64);
}
const pg = Ot(dg, [["render", hg]]),
  mg = $e({
    __name: "Notifier",
    setup(e) {
      const { state: t } = ht(),
        n = (o) => {
          new Audio(`/audio/${o}.mp3`).play();
        };
      return (
        Sc(() => {
          t.notifications.length > 0 &&
            (n(t.notifications[0].status),
            setTimeout(() => {
              t.notifications.pop();
            }, 3e3));
        }),
        (o, s) => {
          const r = It("Icon");
          return (
            V(),
            G("section", null, [
              (V(!0),
              G(
                _e,
                null,
                zn(
                  z(t).notifications,
                  (i, c) => (
                    V(),
                    G(
                      "div",
                      {
                        style: bo([
                          { "z-index": "9999" },
                          { top: c * 15 + "px" },
                        ]),
                        class: Kt([i.status, "noti"]),
                      },
                      [
                        Et(Ce(i.message) + " ", 1),
                        J(
                          r,
                          {
                            icon:
                              i.status === "error"
                                ? "mdi-alert-circle"
                                : i.status === "warning"
                                ? "mdi-alert"
                                : i.status === "success"
                                ? "mdi-check-circle"
                                : "mdi-information-variant",
                            class: "rf scale cp tr absolute",
                            onClick:
                              s[0] || (s[0] = (a) => z(t).notifications.pop()),
                          },
                          null,
                          8,
                          ["icon"]
                        ),
                      ],
                      6
                    )
                  )
                ),
                256
              )),
            ])
          );
        }
      );
    },
  });
const gg = Ot(mg, [["__scopeId", "data-v-96436cb4"]]),
  _g = { key: 0 },
  yg = E("div", { class: "background-green" }, null, -1),
  vg = { class: "main-container" },
  bg = { key: 1 },
  wg = E("h1", null, "Not Authenticated", -1),
  xg = $e({
    __name: "index",
    setup(e) {
      const { state: t } = ht(),
        {
          isAuthenticated: n,
          loginWithRedirect: o,
          getAccessTokenSilently: s,
          user: r,
        } = va();
      Ee(r, async () => {
        r.value ? (t.user = await i()) : (t.user = null);
      });
      const i = async () => {
        const c = await s(),
          l = await (
            await fetch("http://localhost:3000/api/auth?token=" + c)
          ).json();
        return (
          t.notifications.push({
            message: "Welcome " + r.value.name,
            status: "success",
          }),
          l
        );
      };
      return (c, a) => {
        const l = gg,
          u = pg,
          f = tp;
        return (
          V(),
          G(
            _e,
            null,
            [
              J(l),
              z(t).user && z(n)
                ? (V(), G("div", _g, [yg, E("div", vg, [J(u)])]))
                : (V(),
                  G("div", bg, [
                    wg,
                    E(
                      "button",
                      {
                        class: "btn btn-login",
                        onClick:
                          a[0] || (a[0] = Gc((d) => z(o)(), ["prevent"])),
                      },
                      "Login"
                    ),
                  ])),
              J(f),
            ],
            64
          )
        );
      };
    },
  }),
  kg = () => La(() => import("./test-402c7fd2.js"), []),
  Cg = () => La(() => import("./_...all_-2eca044d.js"), []),
  Ig = [
    { name: "test", path: "/test", component: kg, props: !0 },
    { name: "index", path: "/", component: xg, props: !0 },
    { name: "all", path: "/:all(.*)*", component: Cg, props: !0 },
  ],
  Sg = {};
function Eg(e, t) {
  const n = Ma,
    o = It("RouterView");
  return V(), G(_e, null, [J(n), J(o)], 64);
}
const Og = Ot(Sg, [["render", Eg]]);
const Tg = yd({ history: $f("/"), routes: Ig });
mf(Og)
  .use(wd())
  .use(
    Wd({
      domain: "dev-tvhqmk7a.us.auth0.com",
      clientId: "53p0EBRRWxSYA3mSywbxhEeIlIexYWbs",
      authorizationParams: { redirect_uri: window.location.origin },
    })
  )
  .use(Tg)
  .component("Icon", Wh)
  .mount("#app");
export { Ot as _, z as a, G as c, $e as d, V as o, Ce as t, ht as u };
