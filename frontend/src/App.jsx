import { useState } from "react"
import axios from "axios"
import { RadarChart, Radar, PolarGrid, PolarAngleAxis, ResponsiveContainer } from "recharts"

const API = "http://127.0.0.1:8000"

export default function App() {
  const [userId] = useState("tushar")
  const [text, setText] = useState("")
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [tab, setTab] = useState("analyze")
  const [situation, setSituation] = useState("")
  const [questions, setQuestions] = useState([])
  const [answers, setAnswers] = useState(["", ""])
  const [coaching, setCoaching] = useState(null)
  const [socraticStep, setSocraticStep] = useState(1)

  const analyze = async () => {
    if (!text.trim()) return
    setLoading(true)
    try {
      const res = await axios.post(`${API}/analyze/text`, { user_id: userId, text })
      setResult(res.data)
    } catch (e) { alert("Error: " + e.message) }
    setLoading(false)
  }

  const startSocratic = async () => {
    if (!situation.trim()) return
    setLoading(true)
    try {
      const res = await axios.post(`${API}/socratic/start`, { user_id: userId, situation, user_answers: [] })
      setQuestions(res.data.questions)
      setSocraticStep(2)
    } catch (e) { alert("Error: " + e.message) }
    setLoading(false)
  }

  const completeSocratic = async () => {
    setLoading(true)
    try {
      const res = await axios.post(`${API}/socratic/complete`, { user_id: userId, situation, user_answers: answers })
      setCoaching(res.data)
      setSocraticStep(3)
    } catch (e) { alert("Error: " + e.message) }
    setLoading(false)
  }

  const radarData = result ? [
    { subject: "Clarity", value: result.scores.clarity_score },
    { subject: "Structure", value: result.scores.structure_score },
    { subject: "Confidence", value: result.scores.confidence_score },
    { subject: "Persuasiveness", value: result.scores.persuasiveness_score },
  ] : []

  return (
    <div style={{ minHeight: "100vh", background: "#0a0a0a", color: "#e0e0e0", fontFamily: "Georgia, serif", padding: "40px 20px" }}>
      <div style={{ maxWidth: "800px", margin: "0 auto" }}>
        <div style={{ textAlign: "center", marginBottom: "40px" }}>
          <h1 style={{ fontSize: "3rem", color: "#c9a84c", margin: 0, letterSpacing: "4px" }}>THE PRINCE</h1>
          <p style={{ color: "#888", marginTop: "8px", fontStyle: "italic" }}>Strategic Communication Coach</p>
        </div>

        <div style={{ display: "flex", gap: "10px", marginBottom: "30px" }}>
          {["analyze", "coach"].map(t => (
            <button key={t} onClick={() => setTab(t)} style={{
              padding: "10px 24px", border: "1px solid",
              borderColor: tab === t ? "#c9a84c" : "#333",
              background: tab === t ? "#c9a84c22" : "transparent",
              color: tab === t ? "#c9a84c" : "#888",
              cursor: "pointer", borderRadius: "4px",
              textTransform: "capitalize", fontSize: "14px"
            }}>{t === "analyze" ? "Analyze Text" : "Socratic Coach"}</button>
          ))}
        </div>

        {tab === "analyze" && (
          <div>
            <textarea
              value={text} onChange={e => setText(e.target.value)}
              placeholder="Describe a situation or paste something you said/wrote..."
              style={{ width: "100%", height: "140px", background: "#111", border: "1px solid #333", color: "#e0e0e0", padding: "16px", borderRadius: "6px", fontSize: "15px", resize: "vertical", outline: "none", boxSizing: "border-box" }}
            />
            <button onClick={analyze} disabled={loading} style={{ marginTop: "12px", padding: "12px 32px", background: "#c9a84c", color: "#000", border: "none", borderRadius: "4px", cursor: "pointer", fontSize: "15px", fontWeight: "bold", opacity: loading ? 0.6 : 1 }}>
              {loading ? "Analyzing..." : "Analyze"}
            </button>

            {result && (
              <div style={{ marginTop: "30px" }}>
                <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "12px", marginBottom: "24px" }}>
                  {[
                    { label: "Clarity", value: result.scores.clarity_score },
                    { label: "Structure", value: result.scores.structure_score },
                    { label: "Confidence", value: result.scores.confidence_score },
                    { label: "Persuasiveness", value: result.scores.persuasiveness_score },
                  ].map(s => (
                    <div key={s.label} style={{ background: "#111", border: "1px solid #222", borderRadius: "8px", padding: "16px", textAlign: "center" }}>
                      <div style={{ fontSize: "2rem", color: "#c9a84c", fontWeight: "bold" }}>{s.value}</div>
                      <div style={{ fontSize: "12px", color: "#888", marginTop: "4px" }}>{s.label}</div>
                    </div>
                  ))}
                </div>

                <div style={{ background: "#111", border: "1px solid #c9a84c33", borderRadius: "8px", padding: "20px", marginBottom: "20px", textAlign: "center" }}>
                  <div style={{ fontSize: "3rem", color: "#c9a84c" }}>{result.scores.overall_score}<span style={{ fontSize: "1rem", color: "#888" }}>/10</span></div>
                  <div style={{ color: "#888", fontSize: "13px" }}>Overall Score</div>
                </div>

                <div style={{ background: "#111", border: "1px solid #222", borderRadius: "8px", padding: "20px", marginBottom: "20px" }}>
                  <ResponsiveContainer width="100%" height={250}>
                    <RadarChart data={radarData}>
                      <PolarGrid stroke="#333" />
                      <PolarAngleAxis dataKey="subject" tick={{ fill: "#888", fontSize: 12 }} />
                      <Radar dataKey="value" stroke="#c9a84c" fill="#c9a84c" fillOpacity={0.2} />
                    </RadarChart>
                  </ResponsiveContainer>
                </div>

                <div style={{ background: "#111", border: "1px solid #222", borderRadius: "8px", padding: "20px", marginBottom: "16px" }}>
                  <div style={{ color: "#c9a84c", fontSize: "13px", marginBottom: "10px", letterSpacing: "2px" }}>MACHIAVELLI SAYS</div>
                  <p style={{ margin: 0, lineHeight: 1.7, color: "#ccc" }}>{result.scores.machiavelli_feedback}</p>
                </div>

                <div style={{ background: "#111", border: "1px solid #222", borderRadius: "8px", padding: "20px", marginBottom: "16px" }}>
                  <div style={{ color: "#c9a84c", fontSize: "13px", marginBottom: "10px", letterSpacing: "2px" }}>REWRITTEN STRATEGICALLY</div>
                  <p style={{ margin: 0, lineHeight: 1.7, color: "#ccc", fontStyle: "italic" }}>{result.scores.rewritten}</p>
                </div>

                <div style={{ background: "#111", border: "1px solid #222", borderRadius: "8px", padding: "20px" }}>
                  <div style={{ color: "#c9a84c", fontSize: "13px", marginBottom: "10px", letterSpacing: "2px" }}>YOUR PROFILE</div>
                  <div style={{ display: "flex", gap: "20px", flexWrap: "wrap" }}>
                    <span style={{ color: "#888" }}>Sessions: <span style={{ color: "#e0e0e0" }}>{result.profile.total_sessions}</span></span>
                    <span style={{ color: "#888" }}>Improvement: <span style={{ color: result.profile.improvement_rate >= 0 ? "#c9a84c" : "#ff6b6b" }}>
                      {result.profile.improvement_rate >= 0 ? "+" : ""}{result.profile.improvement_rate}%
                    </span></span>
                    <span style={{ color: "#888" }}>Weak areas: <span style={{ color: "#e0e0e0" }}>{JSON.parse(result.profile.weak_areas).join(", ") || "none"}</span></span>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {tab === "coach" && (
          <div>
            {socraticStep === 1 && (
              <div>
                <textarea
                  value={situation} onChange={e => setSituation(e.target.value)}
                  placeholder="Describe a situation where your communication failed or could have been better..."
                  style={{ width: "100%", height: "140px", background: "#111", border: "1px solid #333", color: "#e0e0e0", padding: "16px", borderRadius: "6px", fontSize: "15px", resize: "vertical", outline: "none", boxSizing: "border-box" }}
                />
                <button onClick={startSocratic} disabled={loading} style={{ marginTop: "12px", padding: "12px 32px", background: "#c9a84c", color: "#000", border: "none", borderRadius: "4px", cursor: "pointer", fontSize: "15px", fontWeight: "bold", opacity: loading ? 0.6 : 1 }}>
                  {loading ? "Thinking..." : "Begin Coaching"}
                </button>
              </div>
            )}

            {socraticStep === 2 && (
              <div>
                <div style={{ background: "#111", border: "1px solid #c9a84c33", borderRadius: "8px", padding: "20px", marginBottom: "20px" }}>
                  <div style={{ color: "#c9a84c", fontSize: "13px", marginBottom: "10px", letterSpacing: "2px" }}>REFLECT ON THESE</div>
                  {questions.map((q, i) => (
                    <div key={i} style={{ marginBottom: "20px" }}>
                      <p style={{ color: "#ccc", marginBottom: "8px" }}>{i + 1}. {q}</p>
                      <textarea
                        value={answers[i]}
                        onChange={e => { const a = [...answers]; a[i] = e.target.value; setAnswers(a) }}
                        placeholder="Your answer..."
                        style={{ width: "100%", height: "80px", background: "#0a0a0a", border: "1px solid #333", color: "#e0e0e0", padding: "12px", borderRadius: "6px", fontSize: "14px", resize: "vertical", outline: "none", boxSizing: "border-box" }}
                      />
                    </div>
                  ))}
                  <button onClick={completeSocratic} disabled={loading} style={{ padding: "12px 32px", background: "#c9a84c", color: "#000", border: "none", borderRadius: "4px", cursor: "pointer", fontSize: "15px", fontWeight: "bold", opacity: loading ? 0.6 : 1 }}>
                    {loading ? "Analyzing..." : "Get Strategic Advice"}
                  </button>
                </div>
              </div>
            )}

            {socraticStep === 3 && coaching && (
              <div>
                {[
                  { label: "DIAGNOSIS", value: coaching.diagnosis },
                  { label: "STRATEGIC ADVICE", value: coaching.strategic_advice },
                  { label: "HOW TO HANDLE IT", value: coaching.rewritten },
                  { label: "MACHIAVELLI PRINCIPLE", value: coaching.principle },
                  { label: "YOUR EXERCISE", value: coaching.exercise },
                ].map(item => (
                  <div key={item.label} style={{ background: "#111", border: "1px solid #222", borderRadius: "8px", padding: "20px", marginBottom: "16px" }}>
                    <div style={{ color: "#c9a84c", fontSize: "13px", marginBottom: "10px", letterSpacing: "2px" }}>{item.label}</div>
                    <p style={{ margin: 0, lineHeight: 1.7, color: "#ccc" }}>{item.value}</p>
                  </div>
                ))}
                <button onClick={() => { setSocraticStep(1); setSituation(""); setQuestions([]); setAnswers(["", ""]); setCoaching(null) }}
                  style={{ padding: "10px 24px", background: "transparent", border: "1px solid #c9a84c", color: "#c9a84c", borderRadius: "4px", cursor: "pointer" }}>
                  Start New Session
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}