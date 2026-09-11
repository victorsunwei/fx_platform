flowchart TD



&#x20;   subgraph Core\[FX Platform Core]

&#x20;       PE\[PricingEngine]

&#x20;       MDP\[MarketDataProvider]

&#x20;       AT\[AuditTrail]

&#x20;       EB\[EventBus]

&#x20;       MR\[ModuleRegistry]

&#x20;   end



&#x20;   subgraph PricingModule\[Pricing Module]

&#x20;       PF\[ForwardPricing]

&#x20;       SP\[SpotPricing]

&#x20;       PSandbox\[ModuleSandbox (pricing)]

&#x20;       PCap\[Capabilities (pricing)]

&#x20;   end



&#x20;   subgraph MarketDataModule\[MarketData Module]

&#x20;       MDProv\[MarketData Provider Impl]

&#x20;       MDSandbox\[ModuleSandbox (marketdata)]

&#x20;       MDCap\[Capabilities (marketdata)]

&#x20;   end



&#x20;   subgraph AuditModule\[Audit Module]

&#x20;       AuditImpl\[AuditTrail Impl]

&#x20;       ASandbox\[ModuleSandbox (audit)]

&#x20;       ACap\[Capabilities (audit)]

&#x20;   end



&#x20;   subgraph EventModule\[EventBus Module]

&#x20;       EBSandbox\[ModuleSandbox (eventbus)]

&#x20;       EBCap\[Capabilities (eventbus)]

&#x20;   end



&#x20;   subgraph RegistryModule\[Registry Module]

&#x20;       RegImpl\[ModuleRegistry Impl]

&#x20;       RSandbox\[ModuleSandbox (registry)]

&#x20;       RCap\[Capabilities (registry)]

&#x20;   end



&#x20;   %% Core to Modules

&#x20;   PE --> PF

&#x20;   PE --> SP

&#x20;   PE --> MR



&#x20;   MDP --> MDProv

&#x20;   MDP --> MR



&#x20;   AT --> AuditImpl

&#x20;   AT --> MR



&#x20;   EB --> EBSandbox

&#x20;   EB --> MR



&#x20;   MR --> RegImpl



&#x20;   %% Sandbox and Capabilities

&#x20;   PF --> PSandbox

&#x20;   SP --> PSandbox

&#x20;   PSandbox --> PCap



&#x20;   MDProv --> MDSandbox

&#x20;   MDSandbox --> MDCap



&#x20;   AuditImpl --> ASandbox

&#x20;   ASandbox --> ACap



&#x20;   EBSandbox --> EBCap



&#x20;   RegImpl --> RSandbox

&#x20;   RSandbox --> RCap



&#x20;   %% Events and Audit Flow

&#x20;   MDP --> EB

&#x20;   EB --> AT

&#x20;   AT --> AuditImpl



