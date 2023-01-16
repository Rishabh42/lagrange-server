require("hardhat-deploy")
require("hardhat-deploy-ethers")

const fa = require("@glif/filecoin-address")
const util = require("util")
const request = util.promisify(require("request"))

const DEPLOYER_PRIVATE_KEY = network.config.accounts[0]

function hexToBytes(hex) {
    for (var bytes = [], c = 0; c < hex.length; c += 2) bytes.push(parseInt(hex.substr(c, 2), 16))
    return new Uint8Array(bytes)
}

async function callRpc(method, params) {
    var options = {
        method: "POST",
        url: "https://wallaby.node.glif.io/rpc/v0",
        // url: "http://localhost:1234/rpc/v0",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            jsonrpc: "2.0",
            method: method,
            params: params,
            id: 1,
        }),
    }
    const res = await request(options)
    return JSON.parse(res.body).result
}

const deployer = new ethers.Wallet(DEPLOYER_PRIVATE_KEY)

module.exports = async ({ deployments }) => {
    const { deploy } = deployments

    const priorityFee = await callRpc("eth_maxPriorityFeePerGas")

    // Wraps Hardhat's deploy, logging errors to console.
    const deployLogError = async (title, obj) => {
        let ret
        try {
            ret = await deploy(title, obj)
        } catch (error) {
            console.log(error.toString())
            process.exit(1)
        }
        return ret
    }

    console.log("Wallet Ethereum Address:", deployer.address)

    let token = await deployLogError("LagrangeDAOToken", {
        from: deployer.address,
        args: [],
        maxPriorityFeePerGas: network.name == "wallaby" ? priorityFee : "",
        log: true,
    })

    await deployLogError("SpacePayment", {
        from: deployer.address,
        args: [token.address],
        maxPriorityFeePerGas: network.name == "wallaby" ? priorityFee : "",
        log: true,
    })

    if (token.newlyDeployed) {
        let Token = await ethers.getContractFactory("LagrangeDAOToken")
        let ladToken = Token.attach(token.address)

        let tx = await ladToken.initialize(
            deployer.address,
            network.name == "wallaby"
                ? {
                      gasLimit: 1000000000,
                      maxPriorityFeePerGas: priorityFee,
                  }
                : {}
        )
        console.log("initialize tx:", tx.hash)
    }
}

module.exports.tags = ["LagrangeDAOToken", "SpacePayment"]
