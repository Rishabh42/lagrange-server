require("@nomicfoundation/hardhat-toolbox")
require("hardhat-deploy")
require("hardhat-deploy-ethers")
require("./tasks")
require("dotenv").config({ path: "../.env" })

const PRIVATE_KEY = process.env.private_key
/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
    solidity: "0.8.17",
    defaultNetwork: "wallaby",
    networks: {
        wallaby: {
            url: "https://wallaby.node.glif.io/rpc/v0",
            accounts: [PRIVATE_KEY],
        },
        mumbai: {
            url: process.env.rpc_endpoint,
            accounts: [PRIVATE_KEY],
            gas: 20000000,
            blockGasLimit: 12000000,
        },
    },
    paths: {
        sources: "./contracts",
        tests: "./test",
        cache: "./cache",
        artifacts: "./artifacts",
    },
}
