// Slide 43: MoneyContext with an example exchange rate
package energy

import squants.market.*

given MoneyContext =                         // example rate: 1 EUR = 1.10 USD
  MoneyContext(EUR, defaultCurrencySet, List(CurrencyExchangeRate(EUR(1), USD(1.10))))
