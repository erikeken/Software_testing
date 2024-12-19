from staticfg import CFGBuilder

login_cfg = CFGBuilder().build_from_file("user_login", "./online_shopping_cart/user/user_login.py")
login_cfg.build_visual("./files/cfg/login", "pdf")

logout_cfg = CFGBuilder().build_from_file("user_logout", "./online_shopping_cart/user/user_logout.py")
logout_cfg.build_visual("./files/cfg/logout", "pdf")

auth_cfg = CFGBuilder().build_from_file("auth", "./online_shopping_cart/user/user_authentication.py")
auth_cfg.build_visual("./files/cfg/auth", "pdf")

shop_cfg = CFGBuilder().build_from_file("shop_search", "./online_shopping_cart/shop/shop_search_and_purchase.py")
shop_cfg.build_visual("./files/cfg/shop_search", "pdf")

product_cfg = CFGBuilder().build_from_file("product_search", "./online_shopping_cart/product/product_search.py")
product_cfg.build_visual("./files/cfg/sproduct_search", "pdf")

checkout_cfg = CFGBuilder().build_from_file("checkout", "./online_shopping_cart/checkout/checkout_process.py")
checkout_cfg.build_visual("./files/cfg/checkout", "pdf")

cart_cfg = CFGBuilder().build_from_file("cart", "./online_shopping_cart/checkout/shopping_cart.py")
cart_cfg.build_visual("./files/cfg/cart", "pdf")