export default {
  title: 'RS3 Leveling Guides',
  description: 'Clean, mobile-ready RS3 leveling guides for July 2026',
  srcExclude: ['_agent_memory/**', 'docs/**', 'tasks/**'],
  ignoreDeadLinks: [
    /^\/_agent_memory/,
    /\.\/_agent_memory/
  ],
  themeConfig: {
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Necromancy', link: '/necromancy' },
      { text: 'Ranged', link: '/ranged' },
      { text: 'Melee', link: '/melee' },
      { text: 'Beginner Tips', link: '/sustain-and-tips' },
      { text: 'Gold Making', link: '/money-making' },
      { text: 'RS Wiki', link: 'https://runescape.wiki' }
    ],
    sidebar: {
      '/melee': [
        {
          text: 'Melee 1-120 Guide',
          items: [
            { text: 'Why Melee in 2026', link: '/melee' },
            { text: 'Core Mechanics', link: '/melee#core-mechanics-read-this-once' },
            { text: 'Leveling Route', link: '/melee#leveling-route-1-120' },
            { text: 'Gear Progression', link: '/melee#gear-progression-tables' },
            { text: 'Ability Bars', link: '/melee#ability-bars-revolution-vs-manual' },
            { text: 'Invention Perks', link: '/melee#invention-perks-melee-focused' },
            { text: 'Supporting Skills', link: '/melee#supporting-skills' },
            { text: 'Endgame Gear', link: '/melee#endgame-gear-snapshot-t90-t100' },
            { text: 'Endgame DPS Notes', link: '/melee#endgame-dps-notes-berserk-centric' },
            { text: 'Boss Starter', link: '/melee#short-boss-starter' }
          ]
        }
      ],
      '/necromancy': [
        {
          text: 'Necromancy Guide',
          items: [
            { text: 'Getting Started', link: '/necromancy' },
            { text: 'Quest Order', link: '/necromancy#the-quest-chain-do-these-in-order' },
            { text: 'Combat Training', link: '/necromancy#phase-3-early-combat-training-levels-1-60' },
            { text: 'Gear System', link: '/necromancy#phase-4-gear-progression-the-kili-system' },
            { text: 'Rituals', link: '/necromancy#phase-5-rituals-explained' },
            { text: 'Milestone Map', link: '/necromancy#phase-7-the-level-by-level-milestone-map' },
            { text: 'Supporting Skills', link: '/necromancy#phase-9-supporting-skills-to-train-alongside-necromancy' },
            { text: 'Rasial Boss', link: '/necromancy#phase-8-rasial-the-first-necromancer-endgame-boss' }
          ]
        }
      ],
      '/ranged': [
        {
          text: 'Ranged 1-120 Guide',
          items: [
            { text: 'Overview & Changes', link: '/ranged' },
            { text: '1-120 Leveling Route', link: '/ranged#ranged-leveling-route-1-120' },
            { text: 'Gear Progression', link: '/ranged#gear-progression-tier-1-to-tier-100' },
            { text: 'Ability Bar & Rotations', link: '/ranged#ability-bar-setups-revo-vs-manual' },
            { text: 'Ammunition Meta', link: '/ranged#ammunition-meta-bows-vs-crossbows' },
            { text: 'Invention Perks', link: '/ranged#best-invention-perks-for-ranged' },
            { text: 'Supporting Skills', link: '/ranged#supporting-skills-to-train-alongside-ranged' }
          ]
        }
      ],
      '/sustain-and-tips': [
        {
          text: 'Beginner Survival Guide',
          items: [
            { text: 'Combat Healing & Sustain', link: '/sustain-and-tips#combat-healing-sustain' },
            { text: 'Skilling Sustainability', link: '/sustain-and-tips#skilling-sustainability' },
            { text: 'General New Player Tips', link: '/sustain-and-tips#general-new-player-tips' },
            { text: 'Setting Up Your UI', link: '/sustain-and-tips#essential-settings-ui-layout' }
          ]
        }
      ],
      '/money-making': [
        {
          text: 'Gold Making Guide',
          items: [
            { text: 'Overview & 2026 Changes', link: '/money-making' },
            { text: 'Phase 1: From Zero (F2P)', link: '/money-making#phase-1-starting-from-absolute-zero-f2p-no-requirements' },
            { text: 'Phase 2: Processing', link: '/money-making#phase-2-low-to-mid-stats-processing-1m-5m-starting-budget' },
            { text: 'Phase 3: High-Level', link: '/money-making#phase-3-mid-to-high-level-methods-p2p' },
            { text: 'Weekly/Daily Routine', link: '/money-making#optimized-weekly-daily-routine-post-dailyscape-overhaul' },
            { text: 'GE Flipping', link: '/money-making#ge-flipping-passive-income-layer' }
          ]
        }
      ]
    }
  }
}
