Predstav si, ze si product owner Core Banking Systemu (CBS). Chces vytvorit novy CBS pre banku, ktora sa venuje retailu, ale aj korporatnemu bankovnictvu. Potrebujem vypisat a popisat hlavne funkcionality tohto CBS z dovodu vytvorenia zadania pre dodavatela takehoto systemu. 

Ber do uvahy hlavne core sluzby, ale tiez aj dalsie, ktore bude potrebne vytvorit. Jedna sa o banku, ktora je silna v acquiringu ale aj issuingu.
Tu je komplexný prehľad hlavných funkcionalít pre zadanie dodávateľa CBS. Začnem architektonickým diagramom a potom rozoberiem každú oblasť podrobnejšie.
  ::view-transition-group(*),
  ::view-transition-old(*),
  ::view-transition-new(*) {
    animation-duration: 0.25s;
    animation-timing-function: cubic-bezier(0.19, 1, 0.22, 1);
  }
VvisualizeVvisualize show_widget
1. Správa účtov (Account Management)
Jadro celého CBS. Systém musí podporovať kompletný životný cyklus bankových produktov — od otvorenia až po zrušenie.
Retailové účty: bežné účty (current accounts), sporiace účty, termínované vklady, detské a študentské účty, spoločné účty. Každý typ má vlastnú štruktúru úročenia, poplatkovú schému a pravidlá disponibility.
Korporátne účty: firemné bežné účty, multi-currency účty, nostro/vostro účty, účty pre správu likvidity (notional a physical pooling), escrow účty.
Kľúčové požiadavky: multi-currency, multi-entity architektonická podpora, real-time aktualizácia zostatkov, parametrizovateľné typy produktov bez nutnosti programovania, podpora ISO 20022 dátového modelu.

2. Platobný engine (Payments Processing)
Jedna z najkritickejších komponentov vzhľadom na silnú acquiring pozíciu banky.
Lokálne a SEPA platby: SEPA Credit Transfer (SCT), SEPA Direct Debit (SDD Core a B2B), SEPA Instant Credit Transfer (SCT Inst) s SLA do 10 sekúnd, BACS/TARGET2.
Medzinárodné platby: SWIFT MT a MX (ISO 20022), korešpondenčné bankovníctvo, FX konverzné jadro s real-time kurzmi, tracking a notifikácie stavu platby.
Interné platby: real-time medziúčtové prevody, hromadné platby (bulk processing), stojace príkazy, inkasá. Engine musí zvládnuť vysokú transakčnú záťaž — minimálne 1 000 TPS s latenciou pod 200 ms pre instant platby.

3. Issuing — Vydávanie platobných kariet
Táto oblasť je pre banku strategická a musí byť plnohodnotne riešená natívne v CBS alebo prostredníctvom tesne integrovaného card management systému (CMS).
Typy kariet: debetné karty (Visa/Mastercard/domestic scheme), kreditné karty s revolvingovým aj charge modelom, predplatené karty (single-use aj multi-use), virtuálne karty (primárne pre B2B a eCommerce), korporátne karty s nastaviteľnými limitmi pre jednotlivých zamestnancov.
Card lifecycle management: žiadosť a schválenie, personalizácia a výroba (integrácia s card bureau), aktivácia, blokácia/odblokácia, PIN manažment (online PIN change, PIN reveal), obnova a reissue, zrušenie.
Autorizácia a clearing: real-time autorizačný engine (integrácia na Visa/MC processing sieť), parametrizovateľné autorizačné pravidlá (limity, geografické obmedzenia, merchant category kódy), 3DS 2.x server pre eCommerce transakcie.
Tokenizácia: podpora Apple Pay, Google Pay, Samsung Pay, HCE — integrácia na Token Service Provider (TSP) Visa/Mastercard.
Rewards a lojalita: bodový systém, cashback schémy, kampane — buď natívne, alebo cez integrovanú platformu tretej strany.

4. Acquiring — Akceptácia platobných kariet
Druhý strategický pilier banky. CBS musí pokrývať celý acquiring cyklus.
Merchant management: onboarding obchodníkov vrátane KYB (Know Your Business), správa zmlúv a MDR (Merchant Discount Rate), hierarchická štruktúra obchodníkov (chain, outlet), správa terminálov (TMS integrácia).
Transakčné spracovanie: autorizácia cez sieť Visa/Mastercard (integrácia na scheme processing), clearing a settlement (T+1/T+0), chargeback a dispute management workflow, refund a reversal handling.
POS infraštruktúra: integrácia na TMS pre vzdialenú správu terminálov, podpora kontaktných, bezkontaktných a QR platieb.
eCommerce acquiring: payment gateway, 3DS 2.x issuer a acquirer server, podpora alternatívnych platobných metód (BNPL, digital wallets), podvod detekcia špecifická pre CNP transakcie.
Reporting pre obchodníkov: portál pre obchodníkov s real-time prehľadom transakcií, settlement reporty, reklamačný modul.

5. Úverový modul (Lending)
Retail lending: spotrebné úvery, hypotekárne úvery, kontokorenty, kreditné karty s úverovým rámcom. Systém musí pokrývať celý proces — žiadosť, scoring (integrácia na externé credit bureau: CRIF, SCHUFA), schválenie, čerpanie, splácanie, refinancovanie, delikvenciu a vymáhanie.
Corporate lending: korporátne úvery (bilaterálne aj syndikované), revolvingové kreditné linky, projektové financovanie, leasing, prevádzkové financovanie. Nevyhnutná podpora covenantov, waiverov a amendmentov k zmluvám.
Spoločné požiadavky: parametrizovateľné úrokové schémy (fixná, variabilná, cap/floor, EURIBOR referencing), automatizovaný výpočet RPMN, podpora IFRS 9 impairmentového modelu, integrácia na register záložných práv.

6. Trade Finance a Cash Management (Corporate)
Cash Management: multi-level account pooling (notional a physical), intraday liquidity reporting, cash flow forecasting, ZBA (Zero Balance Account) štruktúry, virtual account management pre korporátnych klientov.
Trade Finance: dokumentárne akreditívy (L/C — import aj export), bankové záruky a záväzkové listy, dokumentárne inkasá, supply chain financing, factoring a forfeiting, integrácia na SWIFT Trade Services Utility (TSU) a platformy ako Komgo.

7. Risk, Fraud a Compliance
AML / CFT: real-time transakčný monitoring, zákazníkový rizikový profil (Customer Risk Rating), PEP a sankčné screeningy (integrácia na World-Check, Dow Jones), SAR workflow (Suspicious Activity Report), podpora regulačného reportingu NBS/ECB.
Fraud management: real-time fraud scoring engine (ML modely), rule-based aj AI-based detekcia, case management pre fraud analytikov, integrácia na Visa/Mastercard fraud siete (Visa Advanced Authorisation, MC Expert Monitoring).
Compliance a regulatory reporting: GDPR compliance (dátové mapy, žiadosti o výmaz/prenos), Basel III/IV kapitálová primeranosť, DORA (digitálna odolnosť), PSD2/PSR compliance, automatizovaný reporting NBS, ECB (FINREP/COREP), FATCA/CRS.

8. Hlavná kniha a Účtovníctvo (General Ledger)
Plnohodnotný accounting engine integrovaný priamo do CBS — nie externý ERP.
Požiadavky: multi-entity, multi-currency, multi-GAAP (IFRS aj lokálne štandardy), automatizované zaúčtovanie pre každý typ transakcie, denné a mesačné uzávierky, intercompany zaúčtovanie, integrácia na externý ERP (SAP, Oracle) cez API, plná auditovateľnosť každého záznamu.

9. Onboarding a KYC/KYB
Retail KYC: digitálny onboarding (web + mobilná aplikácia), eID a video KYC podpora, automatizovaná verifikácia dokladov (OCR + AI), biometrická verifikácia, real-time overenie voči registrom (živnostenský, obchodný, sankčné zoznamy).
Corporate KYB: UBO (Ultimate Beneficial Owner) identifikácia a verifikácia, overenie z obchodných registrov (automatizovaná integrácia), due diligence workflow, pravidelná revízia KYC profilov (Periodic Review), risk-based approach.

10. Kanály a Digital Banking
CBS musí expozovať plnú funkcionalitu cez:
Internet Banking (Web): plnohodnotná správa účtov, platby, kreditné produkty, dokumenty, notifikácie.
Mobile Banking: iOS a Android natívne aplikácie, podpora biometrickej autentifikácie, push notifikácie, in-app customer support.
Open Banking / API: PSD2-compliant API (Account Information Service, Payment Initiation Service), developer portal, sandbox prostredie, OAuth 2.0 a FAPI bezpečnostný profil.
ATM/Cash: ATM driving integrácia (XFS štandard), podpora bezkontaktného výberu (tap & withdraw), cardless výber cez QR/OTP.

11. CRM, Product Catalogue a Pricing Engine
CRM — Customer 360: jednotný pohľad na zákazníka cez všetky produkty, segmentácia, lifecycle management, integrácia na marketingové nástroje.
Product Catalogue: centralizovaná správa bankových produktov a ich parametrov — bez nutnosti programovania pri zavádzaní nových produktov. Parametrizácia úrokových sadzieb, poplatkov, limitov, podmienok.
Pricing Engine: individuálne ceny pre korporátnych klientov (relationship-based pricing), dynamické ceny pre retailové produkty, kampane a špeciálne ponuky.

12. Integračná a Technologická architektura
Toto je pre dodávateľa jedno z kľúčových hodnotiacich kritérií:
API-first architektúra: každá funkcionalita musí byť dostupná ako REST alebo GraphQL API, podpora asynchrónnej komunikácie (Kafka, RabbitMQ).
Core integrácie: VISA/Mastercard scheme siete, SWIFT (FileAct, InterAct, Browse), NBS SIPS (Slovenský interbankový platobný systém), TARGET2/TARGET2-Securities, credit bureau (CRIF), daňový úrad, obchodný register.
Nefunkčné požiadavky: 99,99 % dostupnosť (max 52 min downtime/rok), horizontálna škálovateľnosť, cloud-native alebo cloud-ready architektúra, podpora aktívno-aktívneho datacentra, RTO < 4 hod / RPO < 1 hod.

Súhrn modulov pre zadanie dodávateľa
  ::view-transition-group(*),
  ::view-transition-old(*),
  ::view-transition-new(*) {
    animation-duration: 0.25s;
    animation-timing-function: cubic-bezier(0.19, 1, 0.22, 1);
  }
VvisualizeVvisualize show_widget
Toto je základ zadania pre dodávateľa CBS. Pre finálny RFP (Request for Proposal) dokument by bolo vhodné doplniť ešte tieto sekcie:
Čo doplniť do zadania: detailné SLA a nefunkčné požiadavky (TPS, latencia, dostupnosť), požiadavky na migrčnú stratégiu (prechod zo starého systému), licenčný model (perpetual vs SaaS/cloud), požiadavky na lokalizáciu (slovenské a európske regulačné špecifiká), referenčné inštalácie v obdobných bankách, model podpory a SLA pre produkčné prostredie.
Chceš, aby som niektorú z oblastí rozpracoval podrobnejšie — napríklad do formy detailných user stories, alebo aby som pripravil celý dokument ako formálne zadanie pre dodávateľa (RFP)?Pridaj este pozadovany popis na integracnu vstvu, nakolko banka uvazuje o integracii s partnermi, ktori budu dodavat banke nove sluzby, ktore sama banka neposkytuje. Vytvor zadanie s popisom integracnych vrstiev a poziadaviek.10:33 AMArchitektúrou integračnú vrstvu s API Gateway a partnerským rámcomArchitektúrou integračnú vrstvu s API Gateway a partnerským rámcomVytvorím formálne zadanie ako Word dokument. Najprv pripravím diagram architektúry integračnej vrstvy a potom kompletný .docx dokument.
  ::view-transition-group(*),
  ::view-transition-old(*),
  ::view-transition-new(*) {
    animation-duration: 0.25s;
    animation-timing-function: cubic-bezier(0.19, 1, 0.22, 1);
  }
VvisualizeVvisualize show_widgetTeraz vytvorím kompletný Word dokument so zadaním.Ran 5 commands, edited 2 files, created a fileRan 5 commands, edited 2 files, created a fileDokument je hotový. Tu je prehľad toho, čo zadanie pokrýva v 10 kapitolách:
Štruktúra dokumentu:

Úvod — kontext BaaP stratégie, dôvod samostatnej integračnej vrstvy
Architektonický rámec — 4-vrstvový model (API GW → ESB → Event Streaming → External Connectors), princípy návrhu (API-first, Event-Driven, loose coupling)
API Gateway a Developer Portal — OAuth2/FAPI požiadavky, rate limiting, audit log, samoobslužný onboarding partnerov, sandbox prostredie
ESB / Integration Middleware — routing, protocol transformation, orchestrácia, Saga pattern, Outbox pattern — kompletný katalóg 8 EIP vzorov s prioritou
Event Streaming Platform — Kafka požiadavky, katalóg 30+ domain eventov (účty, platby, karty, KYC, AML...), CDC požiadavky
External Connector Hub — tabuľka všetkých regulačných a schemata integrácií (Visa/MC, SWIFT, NBS, Target2, CRIF, ORSR...)
Partner Ecosystem / BaaP — 6-fázový onboarding framework, 3-tier klasifikácia partnerov, kompletný katalóg plánovaných integrácií (finančné, technologické, prevádzkové)
Bezpečnosť — TLS/mTLS, tokenizácia PAN, IAM, SIEM, penetračné testovanie, PCI DSS v4.x požiadavky
Nefunkčné požiadavky a SLA — dostupnosť, RTO/RPO, throughput, latencia, zoznam protokolov a štandardov
Governance — lifecycle management, API versioning/deprecation policy, GDPR/DORA compliance[CBS_Integracna_Vrstva_Zadanie.docx](https://github.com/user-attachments/files/26372941/CBS_Integracna_Vrstva_Zadanie.docx)
