
from decimal import Decimal, InvalidOperation

#Check whether the trade data is valid.

def validate_trade(trade):
    
    try:
        quantity = Decimal(str(trade["quantity"]))
        price = Decimal(str(trade["price"]))
    except (InvalidOperation, ValueError, TypeError, KeyError):
        return False

    if not quantity.is_finite() or not price.is_finite():
        return False

    if quantity <= 0 or price <= 0:
        return False

    return trade.get("action") in ("Buy", "Sell")

#Check whether the security is restricted for this portfolio.

def check_restricted_security(trade, portfolio):

    return trade["security_id"] in portfolio["restricted_securities"]


def check_sell_holdings(trade, portfolio):
    """Check whether the portfolio has enough quantity to sell."""

    security_id = trade["security_id"]
    requested_quantity = Decimal(str(trade["quantity"]))

    available_quantity = sum(
        (
            Decimal(str(quantity))
            for sid, quantity, _ in portfolio["current_holdings"]
            if sid == security_id
        ),
        Decimal("0")
    )

    return available_quantity >= requested_quantity


#Check whether the portfolio has enough cash for the buy order.

def check_buy_cash(trade, portfolio):
    
    quantity = Decimal(str(trade["quantity"]))
    price = Decimal(str(trade["price"]))

    trade_cost = quantity * price

    return trade_cost <= portfolio["cash_balance"]

#Check whether a buy order exceeds the maximum position limit.

def check_position_concentration(trade, portfolio):

    security_id = trade["security_id"]
    quantity = Decimal(str(trade["quantity"]))
    price = Decimal(str(trade["price"]))

    post_trade_cash = portfolio["cash_balance"] - (quantity * price)

    existing_quantity = sum(
        (
            Decimal(str(qty))
            for sid, qty, _ in portfolio["current_holdings"]
            if sid == security_id
        ),
        Decimal("0")
    )

    post_trade_quantity = existing_quantity + quantity
    post_trade_security_value = post_trade_quantity * price

    value_of_other_holdings = sum(
        (
            Decimal(str(qty)) * Decimal(str(market_price))
            for sid, qty, market_price in portfolio["current_holdings"]
            if sid != security_id
        ),
        Decimal("0")
    )

    total_portfolio_value = (
        post_trade_cash
        + post_trade_security_value
        + value_of_other_holdings
    )

    if total_portfolio_value <= 0:
        return False

    position_pct = post_trade_security_value / total_portfolio_value

    return position_pct > portfolio["max_position_pct"]


def evaluate_trade(trade, portfolio):
    """Evaluate a trade against the portfolio compliance rules."""

    # Step 1: Validate trade data.
    if not validate_trade(trade):
        return {
            "decision": "Rejected",
            "reason": "Invalid trade data."
        }

    # Step 2: Check restricted securities.
    if check_restricted_security(trade, portfolio):
        return {
            "decision": "Rejected",
            "reason": "Security is restricted for this portfolio."
        }

    # Step 3: Check holdings for sell orders.
    if trade["action"] == "Sell":
        if not check_sell_holdings(trade, portfolio):
            return {
                "decision": "Rejected",
                "reason": "Insufficient holdings to sell."
            }

    # Step 4: Check available cash for buy orders.
    if trade["action"] == "Buy":
        if not check_buy_cash(trade, portfolio):
            return {
                "decision": "Rejected",
                "reason": "Insufficient cash for this buy order."
            }

        # Step 5: Check position concentration for buy orders.
        if check_position_concentration(trade, portfolio):
            return {
                "decision": "Needs Manual Sign-off",
                "reason": (
                    "Exceeds maximum position concentration "
                    "— requires approval."
                )
            }

    # Step 6: Approve the trade if all applicable checks pass.
    return {
        "decision": "Approved",
        "reason": "All compliance and execution-readiness checks passed."
    }
