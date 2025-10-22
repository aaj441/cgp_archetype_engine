# Ritual-Union: Technical Architecture Specification

**Document Type:** Technical Design Document
**Version:** 1.0
**Date:** 2025-10-22
**Related:** RITUAL_UNION_BEST_PRACTICES.md

---

## Executive Summary

Ritual-Union is a sound therapy engine designed with three core architectural principles:

1. **Privacy-First Biometric Processing:** All health data processed locally; minimal cloud dependency
2. **Modular Agent System (Pantheon XII):** Loosely coupled domain modules with event-driven communication
3. **ADHD-Optimized UX Layer:** Minimalist interface prioritizing audio/haptic feedback over visual complexity

This document defines the technical architecture to achieve these goals.

---

## System Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                      USER INTERFACE LAYER                     │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐  │
│  │  Ritual UI  │  │  Sound Mixer │  │  Settings/Profile  │  │
│  │  (Hestia)   │  │  (Apollo UI) │  │     (Demeter)      │  │
│  └─────────────┘  └──────────────┘  └────────────────────┘  │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         │ Event Bus (Hermes)
                         │
┌────────────────────────▼─────────────────────────────────────┐
│                   ORCHESTRATION LAYER                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │            Pantheon Agent Coordinator                 │   │
│  │  (Message routing, state synchronization)            │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌────────┐            │
│  │ Apollo  │ │Artemis  │ │Demeter  │ │Poseidon│   ...      │
│  │ (Music) │ │(Ritual) │ │(Health) │ │ (Data) │            │
│  └─────────┘ └─────────┘ └─────────┘ └────────┘            │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         │ Domain Services
                         │
┌────────────────────────▼─────────────────────────────────────┐
│                     DOMAIN LAYER                              │
│  ┌───────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│  │ Sound Engine  │  │  Ritual Engine   │  │  Biometric   │  │
│  │ (Adaptive     │  │  (Sequencer,     │  │  Analyzer    │  │
│  │  Composition) │  │   Timer, Haptic) │  │  (HR, RR)    │  │
│  └───────────────┘  └──────────────────┘  └──────────────┘  │
│                                                               │
│  ┌───────────────┐  ┌──────────────────┐                    │
│  │ Personalization│  │  Archetype Model │                    │
│  │ Engine        │  │  (User Profiles)  │                    │
│  └───────────────┘  └──────────────────┘                    │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         │ Data Access
                         │
┌────────────────────────▼─────────────────────────────────────┐
│                  INFRASTRUCTURE LAYER                         │
│  ┌─────────────┐ ┌────────────┐ ┌─────────────────────────┐ │
│  │  HealthKit  │ │ Last.fm/   │ │  Local Storage         │ │
│  │  Adapter    │ │ Spotify    │ │  (SQLite/Realm)        │ │
│  │             │ │ Adapter    │ │                         │ │
│  └─────────────┘ └────────────┘ └─────────────────────────┘ │
│                                                               │
│  ┌─────────────┐ ┌────────────┐                             │
│  │  Audio I/O  │ │  Cloud Sync│                             │
│  │  (Native)   │ │  (Optional)│                             │
│  └─────────────┘ └────────────┘                             │
└──────────────────────────────────────────────────────────────┘
```

---

## Pantheon XII Agent Specifications

### Agent Communication Contract

**Message Structure:**
```typescript
interface PantheonMessage {
  id: string;              // UUID
  timestamp: number;       // Unix timestamp
  source: AgentType;       // e.g., "Apollo", "Artemis"
  destination: AgentType | "broadcast";
  event: string;           // e.g., "heart_rate_changed", "ritual_started"
  payload: any;            // Event-specific data
  metadata?: {
    sessionId?: string;
    userId?: string;
    priority?: "low" | "normal" | "high";
  };
}
```

**Event Bus (Hermes Implementation):**
- Pub/Sub pattern with typed event channels
- Agents subscribe to specific event types
- No direct agent-to-agent coupling
- Event history for debugging (last 100 messages)

---

### Core Agent Definitions

#### Apollo (Music & Resonance)

**Responsibility:** Generate and modulate adaptive soundscapes

**Inputs:**
- Biometric state (from Demeter)
- User mood selection
- Time of day
- Ritual phase (from Artemis)

**Outputs:**
- Audio buffer stream
- Soundscape metadata (tempo, key, intensity)

**Internal Components:**
```
Apollo/
├── SoundscapeGenerator
│   ├── LayerMixer (ambient, rhythmic, melodic, nature)
│   ├── AdaptiveModulator (tempo, pitch, volume adjustments)
│   └── TransitionEngine (crossfade logic)
├── AudioLibrary
│   ├── PreloadedSamples (core sounds, offline-ready)
│   └── StreamingAssets (extended library)
└── EffectsProcessor
    ├── Reverb, Delay, Filter (contextual effects)
    └── SpatialAudio (3D positioning)
```

**Key Algorithms:**
- **Heart Rate → Tempo Mapping:**
  ```
  targetTempo = baselineBPM + (currentHR - restingHR) * 0.8
  Clamp between 40-120 BPM
  ```
- **Circadian Brightness:**
  ```
  Morning (6-10am): +20% brightness (more high frequencies)
  Midday (10am-3pm): neutral
  Evening (6-10pm): -30% brightness (warmer, lower frequencies)
  Night (10pm-6am): -50% brightness (deep ambient)
  ```

---

#### Artemis (Focus & Ritual Design)

**Responsibility:** Orchestrate micro-rituals and manage focus sessions

**Inputs:**
- User ritual selection
- Current energy state (from Demeter)
- Calendar context (optional)

**Outputs:**
- Ritual sequence commands
- Haptic feedback patterns
- Timer state updates

**Ritual Schema:**
```typescript
interface Ritual {
  id: string;
  name: string;
  duration: number; // seconds
  archetype?: string; // e.g., "Griefwalker", "Solo Architect"
  phases: RitualPhase[];
  adaptiveParams?: {
    extendIfCalm?: boolean; // Extend if HR drops significantly
    skipIfAgitated?: string[]; // Skip certain phases if HR elevated
  };
}

interface RitualPhase {
  type: "breath" | "reflection" | "movement" | "intention" | "release";
  duration: number;
  audioRequest: {
    soundscape: string;
    intensity: number; // 0-1
  };
  hapticPattern?: HapticRhythm;
  prompt?: {
    text: string;
    voiceEnabled?: boolean;
  };
}
```

**Haptic Patterns:**
```typescript
type HapticRhythm = {
  pattern: "steady" | "breathing" | "pulse" | "wave";
  bpm?: number; // If rhythmic
  intensity: number; // 0-1
};

// Example: Breathing rhythm for 4-7-8 technique
{
  pattern: "breathing",
  sequence: [
    { type: "light", duration: 4000 }, // Inhale
    { type: "none", duration: 7000 },  // Hold
    { type: "medium", duration: 8000 } // Exhale
  ]
}
```

---

#### Demeter (Health & Rhythm)

**Responsibility:** Analyze biometric data and classify energy states

**Inputs:**
- HealthKit data stream (HR, respiratory rate, movement, sleep)
- Time of day
- Historical patterns

**Outputs:**
- Current energy state classification
- Circadian phase
- Stress indicators
- Personalized baselines

**Energy State Model:**
```typescript
type EnergyState =
  | "depleted"      // HR low, movement minimal → rest needed
  | "calm"          // HR near baseline, steady → maintenance
  | "focused"       // HR slightly elevated, low variability → flow state
  | "energized"     // HR elevated, high variability → active engagement
  | "overstimulated"; // HR high, rapid changes → need calming

interface BiometricSnapshot {
  heartRate: number;
  heartRateVariability?: number; // SDNN in ms
  respiratoryRate?: number;      // Breaths per minute
  movement: "sedentary" | "light" | "moderate" | "vigorous";
  timestamp: Date;
}
```

**Baseline Calculation:**
- Rolling 7-day average for resting HR
- Time-of-day normalization (HR naturally higher in afternoon)
- Outlier rejection (discard top/bottom 5%)

**Stress Detection:**
```
IF heartRate > (baseline + 15) AND hrv < (baseline_hrv - 20)
  → Likely stressed
  → Recommend calming ritual
```

---

#### Poseidon (Data Flow)

**Responsibility:** Orchestrate external data sources and sync

**Inputs:**
- API credentials (Last.fm, Spotify, Apple Music)
- Sync configuration

**Outputs:**
- Music listening history
- Mood inferences from music taste
- Sync status updates

**Data Pipelines:**
```
Last.fm → Recent Tracks → Mood Analysis → User Profile Update
                ↓
          Valence/Energy classification
          (Spotify Audio Features API)
                ↓
          Weight toward soundscape preferences
```

**Privacy Controls:**
- All API tokens encrypted in Keychain (iOS) / Keystore (Android)
- User can disconnect services anytime
- No data persisted in cloud without explicit opt-in

---

#### Hestia (Calm UX & Space)

**Responsibility:** UI component library with ADHD-friendly defaults

**Design System:**
```
Colors:
  - Primary: Soft indigo (#6366F1) — calming, trustworthy
  - Secondary: Warm amber (#F59E0B) — energizing, gentle
  - Background: Off-white (#FAFAF9) or Deep charcoal (#1F2937)
  - Accent: Muted coral (#FB7185) — emotional warmth

Typography:
  - Headings: Inter (clean, readable)
  - Body: System default or OpenDyslexic (user choice)
  - Sizes: 18px base (mobile), 16px base (desktop)

Spacing:
  - Base unit: 8px
  - Generous padding (24-32px) to avoid claustrophobia
  - Touch targets: minimum 44x44px (iOS HIG)

Motion:
  - All animations: 200-300ms easing
  - Respect prefers-reduced-motion
  - Subtle fades, avoid sudden pops
```

**Component Library:**
- `RitualCard`: Swipeable ritual selector with audio preview
- `SoundscapeSlider`: Visual waveform representing current audio
- `EnergyIndicator`: Biometric-driven circular gauge (calm → energized)
- `HapticButton`: Buttons with tactile feedback
- `MinimalTimer`: Clean countdown with progress ring

---

## Data Models

### User Profile Schema

```typescript
interface UserProfile {
  id: string;
  archetype?: ArchetypeType; // Primary CGP archetype
  preferences: {
    defaultSoundscape: string;
    hapticEnabled: boolean;
    voicePromptsEnabled: boolean;
    theme: "light" | "dark" | "auto";
    fontChoice: "system" | "opendyslexic";
  };
  biometricBaselines: {
    restingHeartRate: number;
    averageHRV: number;
    sleepSchedule: { bedtime: string; wakeTime: string };
  };
  ritualHistory: RitualSession[];
  connectedServices: {
    healthKit: { authorized: boolean; dataTypes: string[] };
    lastFm?: { username: string; connected: boolean };
    spotify?: { connected: boolean };
  };
  privacySettings: {
    allowCloudSync: boolean;
    allowAnonymousAnalytics: boolean;
  };
}
```

### Ritual Session Schema

```typescript
interface RitualSession {
  id: string;
  ritualId: string;
  startTime: Date;
  endTime?: Date;
  completed: boolean;
  initialEnergyState: EnergyState;
  finalEnergyState?: EnergyState;
  biometricSnapshots: BiometricSnapshot[];
  userFeedback?: {
    helpfulness: 1 | 2 | 3 | 4 | 5; // Simple rating
    tags?: string[]; // "too-fast", "just-right", "fell-asleep"
  };
}
```

---

## Technology Stack Recommendations

### Option 1: React Native (Cross-Platform)

**Rationale:** Fastest to market, good for web + mobile

**Stack:**
```yaml
Framework: React Native (Expo managed workflow)
Language: TypeScript
Audio Engine:
  - expo-av (basic playback)
  - react-native-track-player (background audio)
  - Custom Tone.js integration (web)
Biometrics:
  - react-native-health (iOS HealthKit)
  - react-native-google-fit (Android)
State Management: Zustand (lightweight, simple)
Storage:
  - AsyncStorage (small data)
  - WatermelonDB (complex queries, large datasets)
UI Library:
  - React Native Paper (Material Design baseline)
  - Custom Hestia components
Haptics: expo-haptics
Testing: Jest + React Native Testing Library
```

**Pros:**
- Single codebase for iOS, Android, web
- Large community, extensive libraries
- Hot reload for rapid iteration

**Cons:**
- Audio latency higher than native (acceptable for ambient soundscapes)
- HealthKit integration requires native modules
- Performance ceiling lower than Swift/Kotlin

---

### Option 2: Swift/SwiftUI (iOS-First)

**Rationale:** Best performance, deepest HealthKit integration

**Stack:**
```yaml
Framework: SwiftUI
Language: Swift
Audio Engine: AVAudioEngine + AVFoundation
Biometrics: HealthKit (native)
State Management: Combine + @StateObject/@ObservedObject
Storage: Core Data or Realm
UI: Custom Hestia design system (SwiftUI components)
Haptics: Core Haptics
Backend: Firebase (if needed) or Supabase
Testing: XCTest + SwiftUI Previews
```

**Pros:**
- Lowest audio latency (<10ms)
- Native HealthKit—no abstraction layer
- Best Apple Watch integration
- Superior performance

**Cons:**
- iOS-only (need separate Android app)
- Smaller talent pool (Swift developers)
- Slower iteration vs. hot reload

---

### Option 3: Progressive Web App (Web-First Prototype)

**Rationale:** Fastest validation, no app store friction

**Stack:**
```yaml
Framework: Next.js 15 (React + SSR)
Language: TypeScript
Audio Engine: Tone.js + Web Audio API
Biometrics:
  - Web Bluetooth API (limited devices)
  - Manual input fallback
State Management: Zustand or Jotai
Storage: IndexedDB (Dexie.js)
UI: Tailwind CSS + Hestia components
PWA: Workbox (offline support)
Hosting: Vercel or Cloudflare Pages
```

**Pros:**
- Zero install friction (URL share)
- Easiest A/B testing
- Works on desktop + mobile

**Cons:**
- No native HealthKit access (deal-breaker for full biometric integration)
- Limited background audio on iOS Safari
- No haptic feedback API

---

## Recommended Path Forward

### Hybrid Approach: Web Prototype → React Native MVP → Native Optimization

**Phase 1: Web Prototype (2-3 weeks)**
- Build core ritual experience with Tone.js
- Manual biometric input (sliders for HR, mood)
- Validate soundscape adaptation logic
- User testing with 10-20 beta users

**Phase 2: React Native MVP (4-6 weeks)**
- Port web prototype to React Native
- Integrate HealthKit (iOS) + Google Fit (Android)
- Implement full Pantheon agent system
- Launch to 100-person beta (TestFlight + Google Play Internal Testing)

**Phase 3: Native Optimization (Optional, 8+ weeks)**
- If audio latency becomes issue → Swift audio engine
- If Apple Watch integration critical → native iOS companion
- Keep React Native for 80% of features, optimize hot paths

---

## Security & Privacy Architecture

### Data Classification

| Data Type | Storage | Encryption | Cloud Sync | Retention |
|-----------|---------|------------|------------|-----------|
| Health metrics (HR, RR) | Local only | AES-256 at rest | Never | 30 days rolling |
| Ritual sessions | Local + opt-in cloud | AES-256 | User choice | Indefinite (user-controlled) |
| User preferences | Local + cloud | AES-256 | Auto | Indefinite |
| Audio files | Local cache | None (public assets) | CDN | Cache eviction after 7 days |
| API tokens | Keychain/Keystore | OS-managed | Never | Until user disconnects |

### Compliance Checklist

- [ ] **GDPR Article 17 (Right to Erasure):** In-app "Delete All Data" button
- [ ] **HIPAA (if storing PHI):** Sign BAA with cloud provider, implement audit logs
- [ ] **CCPA (California users):** Data export in JSON format, opt-out of analytics
- [ ] **Apple App Store:** Privacy nutrition labels, HealthKit usage description
- [ ] **Accessibility:** WCAG 2.2 Level AAA compliance

---

## Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| App launch to first sound | <2 seconds | Time to AudioContext.resume() |
| Biometric → soundscape update | <50ms | Event timestamp delta |
| Ritual phase transition | <100ms | Haptic + audio sync latency |
| Battery drain (30 min session) | <5% | iOS Battery API |
| Memory footprint | <100MB | Xcode Instruments |
| Crash-free rate | >99.5% | Firebase Crashlytics |

---

## Testing Strategy

### Unit Tests
- Biometric analysis algorithms (Demeter)
- Soundscape modulation logic (Apollo)
- Ritual sequencing (Artemis)
- Coverage target: >80% for domain layer

### Integration Tests
- HealthKit data flow → energy state classification
- Event bus message routing (Hermes)
- Soundscape transitions during ritual

### E2E Tests (Detox or Maestro)
- Complete ritual from start to finish
- Biometric permission flows
- Offline functionality

### Accessibility Tests
- VoiceOver navigation (iOS)
- TalkBack navigation (Android)
- Keyboard-only navigation (web)
- Color contrast validation

### User Testing
- **Prototype stage:** 5 moderated sessions (think-aloud protocol)
- **Beta stage:** 50 unmoderated sessions (analytics + surveys)
- **Post-launch:** Continuous feedback loop via in-app prompts

---

## Deployment Architecture

### Continuous Integration

```yaml
# .github/workflows/ci.yml
name: CI/CD
on: [push, pull_request]

jobs:
  test:
    runs-on: macos-latest
    steps:
      - Checkout code
      - Setup Node.js / Xcode
      - Run unit tests
      - Run linter (ESLint/SwiftLint)
      - Upload coverage to Codecov

  build-ios:
    runs-on: macos-latest
    steps:
      - Build iOS app (Xcode)
      - Run E2E tests (Detox)
      - Upload to TestFlight (if main branch)

  build-android:
    runs-on: ubuntu-latest
    steps:
      - Build Android APK/AAB
      - Run E2E tests
      - Upload to Google Play Internal Testing
```

### Environment Configuration

```
Development:
  - Local HealthKit simulator data
  - Mock Last.fm API responses
  - Hot reload enabled

Staging:
  - TestFlight / Google Play Internal Testing
  - Real HealthKit data (beta testers)
  - Analytics enabled (Mixpanel/Amplitude)

Production:
  - App Store / Google Play
  - Crash reporting (Sentry/Crashlytics)
  - Feature flags (LaunchDarkly) for gradual rollout
```

---

## Open Questions & Decisions Needed

1. **Platform Priority:** iOS-first, Android-first, or simultaneous?
   - **Recommendation:** iOS-first (better HealthKit integration, ADHD app precedent)

2. **Monetization Model:**
   - Freemium (3 rituals free, $4.99/month for full library)?
   - One-time purchase ($9.99)?
   - Completely free (Aaron OS ecosystem play)?

3. **Voice Prompts:**
   - Pre-recorded human voice?
   - Text-to-speech (accessibility benefit)?
   - No voice (text + haptic only)?

4. **Apple Watch Companion:**
   - Required for v1 or post-launch?
   - **Recommendation:** Post-launch (reduces scope, nice-to-have)

5. **Cloud Sync:**
   - Firebase (easy, vendor lock-in)?
   - Supabase (privacy-focused, open-source)?
   - iCloud (iOS-only, free tier generous)?

---

## Conclusion

This architecture balances three competing priorities:

1. **Rapid validation** (web prototype, then React Native)
2. **Privacy-first design** (local processing, minimal cloud)
3. **Neurodivergent-friendly UX** (ADHD-optimized, audio-first)

The Pantheon XII modular system ensures we can iterate on individual agents (e.g., improve Apollo's soundscape algorithm) without touching other modules.

**Next step:** Choose platform (web vs. React Native vs. Swift) based on:
- Development timeline constraints
- Target user platform distribution (iOS-heavy or Android-heavy?)
- Team technical expertise

Once platform is chosen, proceed to **Phase 1 implementation** (see RITUAL_UNION_BEST_PRACTICES.md roadmap).

---

**Document Maintainer:** Claude (Athena + Hephaestus mode)
**Review Cycle:** Weekly during active development
**Stakeholders:** Aaron OS Product Team, Pantheon XII Agents
