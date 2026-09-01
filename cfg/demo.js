/* BB CLIENT LIBRARY · demo cast.
   FICTIONAL client, fictional links, per the demo rule: no real client data
   enters a cast until scripts/pull-month.py bakes it from the live systems.
   No PIN since 2026-09-01: the library opens straight from the link. */
window.CFG = {
  meta: {
    slug: "demo",
    name: "Cinnamon & Co",
    wa: "94766584993",
    updated: "30 August 2026"
  },
  theme: { brand: "#8a5a2b", "brand-soft": "#f5ede2", "brand-glow": "rgba(138,90,43,.3)",
    logo: "assets/clients/demo.svg" },
  copy: {
    hello: "Hello, Cinnamon team.",
    sub: "Everything we have produced for you, in one place."
  },
  months: [
    { id: "2026-08", label: "August",
      videos: [
        { title: "Signature blend, launch film", note: "Final cut · 42 seconds", drive: "https://drive.google.com/drive/folders/demo-aug-v1", added: "2026-08-28" },
        { title: "Behind the roastery", note: "Reel · 28 seconds", drive: "https://drive.google.com/drive/folders/demo-aug-v2", added: "2026-08-21" }
      ],
      posts: [
        { title: "The morning ritual carousel", date: "28 Aug", platform: "Instagram", link: "https://www.instagram.com/p/demo1", added: "2026-08-28" },
        { title: "Meet the roaster", date: "21 Aug", platform: "Instagram", link: "https://www.instagram.com/p/demo2", added: "2026-08-21" },
        { title: "Weekend tasting flight", date: "14 Aug", platform: "Facebook", link: "https://www.facebook.com/demo3", added: "2026-08-14" }
      ]
    },
    { id: "2026-07", label: "July",
      videos: [
        { title: "Cold brew, three ways", note: "Reel · 31 seconds", drive: "https://drive.google.com/drive/folders/demo-jul-v1", added: "2026-07-24" }
      ],
      posts: [
        { title: "Origin story, part one", date: "24 Jul", platform: "Instagram", link: "https://www.instagram.com/p/demo4", added: "2026-07-24" },
        { title: "Iced season opener", date: "10 Jul", platform: "Instagram", link: "https://www.instagram.com/p/demo5", added: "2026-07-10" }
      ]
    },
    /* an older year, so the demo exercises the month labels growing a year
       once a library spans more than one. A real cast gets this from its
       own data, never from a fixture. */
    { id: "2025-12", label: "December",
      videos: [
        { title: "Gifting season film", note: "Final cut · 38 seconds", drive: "https://drive.google.com/drive/folders/demo-dec-v1", added: "2025-12-12" }
      ],
      posts: [
        { title: "The hamper, unwrapped", date: "18 Dec", platform: "Instagram", link: "https://www.instagram.com/p/demo6", added: "2025-12-18" }
      ]
    }
  ],
  docs: [
    { title: "August performance report", kind: "Monthly report", date: "Aug 2026", href: "https://example.com/demo-report", added: "2026-08-30" },
    { title: "Quarter plan, October to December", kind: "Strategy", date: "Aug 2026", href: "https://example.com/demo-quarter", added: "2026-08-30" },
    { title: "Your customer profile", kind: "ICP", date: "Jul 2026", href: "https://example.com/demo-icp", added: "2026-07-20" }
  ],
  facts: [
    { k: "What you sell", v: "Single origin Ceylon cinnamon and coffee, retail and wholesale", g: "Business", added: "2026-08-15" },
    { k: "Who buys", v: "Colombo households and boutique hotels, gifting spikes in December", g: "Audience", added: "2026-08-15" },
    { k: "Your voice", v: "Warm, craft first, never discount led", g: "Brand voice", added: "2026-08-15" },
    { k: "House rule", v: "Provenance claims always name the estate", g: "Guardrails", added: "2026-08-30" }
  ],
  factsReviewed: "30 August 2026",
  beacon: null
};
