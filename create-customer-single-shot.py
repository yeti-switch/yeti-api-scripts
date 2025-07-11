import yeti_switch_api
from config import init
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
                    prog='create-customer-single-shot',
                    description='Creating Yeti customer objects'
             )
    parser.add_argument('-c', '--customer', required=True, type=str, help='Customer name to create')
    parser.add_argument('-i', '--ip', required=False, type=str, help='Customer IP to create Customer Auth')
    parser.add_argument('-r', '--routing-plan', required=False, type=int, help='Routing Plan ID create Customer Auth')
    parser.add_argument('-p', '--rateplan', required=False, type=int, help='Customer IP to create Customer Auth')

    #    parser.print_help()
    args = parser.parse_args()
    #process(args.rest, output=args.output, verbose=args.verbose)

cfg = init()

yeti_switch_api.orm.OrmClient({
    'API_ROOT': cfg.api.endpoint,
    'AUTH_CREDS': {
        'login': cfg.api.user,
        'password': cfg.api.password,
    },
    'VALIDATE_SSL': True,
    'TIMEOUT': 10,
})

yeti_switch_api.orm.OrmClient.auth.refresh_token()

customer_name = args.customer
acc_name = customer_name+'-acc'
gw_name = customer_name+'-gw'

contractor = yeti_switch_api.orm.Contractor()
contractor.name = customer_name
contractor.customer = True
contractor.vendor = False
contractor.enabled = True
contractor.create()

gw = yeti_switch_api.orm.Gateway()
gw.name = gw_name
gw.contractor = contractor
gw.enabled = True
gw.allow_termination = False
gw.allow_origination = True
gw.create()

timezone = yeti_switch_api.orm.Timezone.from_id(1)
acc = yeti_switch_api.orm.Account()
acc.name = acc_name
acc.contractor = contractor
acc.timezone = timezone
acc.min_balance = -100
acc.max_balance = 100
acc.create()

def get_rateplan(id):
    rp = yeti_switch_api.orm.Rateplan.from_id(str(id))

    if rp.name is None:
        raise Exception("Rateplan doesn't exists")
   
    return rp

def get_routing_plan(id):
    routing_plan = yeti_switch_api.orm.RoutingPlan.from_id(str(id))

    if routing_plan.name is None:
        raise Exception("RoutingPlan doesn't exists")

    return routing_plan


def create_ca():
    print("Creating Customer Auth")
    ca = yeti_switch_api.orm.CustomersAuth()
    ca.name = customer_name+'-ca'
    ca.ip = [ args.ip ]
    ca.customer = contractor
    ca.account = acc
    ca.gateway = gw

    ca.rateplan = get_rateplan(args.rateplan)
    ca.routing_plan = get_routing_plan(args.routing_plan)

    ca.create()

if args.ip is not None and args.routing_plan is not None and args.rateplan is not None:
    create_ca()
