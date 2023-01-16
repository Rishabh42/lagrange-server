const { expect } = require("chai")
const { upgrades } = require("hardhat")

describe("SpacePayment", function () {
    // We define a fixture to reuse the same setup in every test.
    // We use loadFixture to run this setup once, snapshot that state,
    // and reset Hardhat Network to that snapshot in every test.
    // async function deployContracts() {
    // Contracts are deployed using the first signer/account by default

    //  return { renFil, nft, owner, otherAccount }
    // }

    let token
    let payment
    let accounts
    let u1

    describe("Deployment", function () {
        it("Should set the right owner", async function () {
            accounts = await ethers.getSigners()
            u1 = accounts[0].address

            let Token = await ethers.getContractFactory("LagrangeDAOToken")
            token = await Token.deploy()

            let SpacePayment = await ethers.getContractFactory("SpacePayment")
            payment = await SpacePayment.deploy(token.address)
            await payment.deployed()
            //const { nft, owner } = await loadFixture(deployContracts)

            expect(await payment.owner()).to.equal(u1)
        })

        it("Should mint tokens", async function () {
            accounts = await ethers.getSigners()

            await token.initialize(u1)
            let balance = await token.balanceOf(u1)

            expect(balance).to.equal(ethers.utils.parseEther("150000000"))
        })
    })

    describe("Spaces", () => {
        it("Try buying space without deposit", async () => {
            let balance = await payment.balanceOf(u1)
            expect(balance).to.equal(0)
            await expect(payment.buySpace(2, 1)).to.be.revertedWith("not enough balance")
        })

        it("Should deposit tokens", async () => {
            await token.approve(payment.address, ethers.utils.parseEther("1000"))
            await payment.deposit(ethers.utils.parseEther("1000"))

            let balance = await payment.balanceOf(u1)
            expect(balance).to.equal(ethers.utils.parseEther("1000"))

            let tokenBalance = await token.balanceOf(u1)
            expect(tokenBalance).to.equal(ethers.utils.parseEther("149999000"))
        })

        it("Should buy space", async () => {
            await payment.buySpace(3, 3)

            let balance = await payment.balanceOf(u1)
            expect(balance).to.equal(ethers.utils.parseEther("940"))

            let info = await payment.spaceInfo(0)
            expect(info.owner).to.equal(u1)
        })
    })
})
